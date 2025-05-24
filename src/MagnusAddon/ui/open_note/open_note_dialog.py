from __future__ import annotations

import threading
from typing import Callable, Optional, TypeVar

from ankiutils.app import col
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.sentences.sentencenote import SentenceNote
from note.vocabulary.vocabnote import VocabNote
from PyQt6.QtCore import Qt, QTimer, pyqtBoundSignal
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from sysutils import ex_str, typed


class NoteSearchDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Find Notes")
        self.resize(1800, 1100)

        self.matched_notes: list[JPNote] = []
        self._lock = threading.Lock()

        layout = QVBoxLayout(self)

        # Create search input field
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search for notes...")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Create results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Type", "Question", "Answer"])
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.results_table)

        # Setup delayed searching (for real-time results as user types)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(200)  # 200ms delay
        typed.checked_cast(pyqtBoundSignal, self.search_timer.timeout).connect(self.perform_search)

        # Connect signals
        typed.checked_cast(pyqtBoundSignal, self.search_input.textChanged).connect(self.on_search_text_changed)
        typed.checked_cast(pyqtBoundSignal, self.results_table.cellDoubleClicked).connect(self.on_cell_double_clicked)
        # Add selection change signal to handle keyboard/mouse selection
        typed.checked_cast(pyqtBoundSignal, self.results_table.itemSelectionChanged).connect(self.on_selection_changed)

        self.search_input.setFocus()

    def on_search_text_changed(self, _text: str) -> None:
        if self.search_timer.isActive():
            self.search_timer.stop()
        self.search_timer.start()

    def perform_search(self) -> None:
        with self._lock:
            """Perform the actual search and update the results table"""
            search_text = self.search_input.text().strip().lower()
            if not search_text:
                self.results_table.setRowCount(0)
                self.matched_notes = []
                return

            # Get the JP collection
            matching_notes: list[JPNote] = []

            max_notes = 60

            def note_question(note: JPNote) -> str: return ex_str.strip_html_and_bracket_markup(note.get_question())
            def note_answer(note: JPNote) -> str: return ex_str.strip_html_and_bracket_markup(note.get_answer())
            def kanji_readings(note: KanjiNote) -> str: return " ".join(note.get_readings_clean())
            def vocab_readings(vocab: VocabNote) -> str: return " ".join(vocab.readings.get())
            def vocab_forms(vocab: VocabNote) -> str: return " ".join(vocab.forms.without_noise_characters())

            # Search in kanji notes
            matching_notes.extend(self._search_in_notes(
                max_notes - len(matching_notes),
                col().kanji.all(),
                search_text,
                note_question,
                note_answer,
                kanji_readings
            ))

            # Search in vocab notes
            matching_notes.extend(self._search_in_notes(
                max_notes - len(matching_notes),
                col().vocab.all(),
                search_text,
                note_question,
                note_answer,
                vocab_forms,
                vocab_readings
            ))

            # Search in sentence notes
            matching_notes.extend(self._search_in_notes(
                max_notes - len(matching_notes),
                col().sentences.all(),
                search_text,
                note_question,
                note_answer,
            ))

            self.matched_notes = matching_notes
            self._update_results_table()

    TNote: TypeVar = TypeVar("TNote", bound=JPNote)
    @staticmethod
    def _search_in_notes(max_notes: int, notes: list[TNote], search_text: str, *extractors: Callable[[TNote], str]) -> list[JPNote]:
        matches: list[JPNote] = []

        if max_notes <= 0:
            return []

        clean_search = ex_str.strip_html_and_bracket_markup(search_text)

        for note in notes:
            for extractor in extractors:
                field_text = extractor(note)
                clean_field = ex_str.strip_html_and_bracket_markup(field_text)
                if clean_search in clean_field:
                    matches.append(note)
                    if len(matches) >= max_notes:
                        return matches
                    break

        return matches

    @staticmethod
    def _create_item(text: str) -> QTableWidgetItem:
        item = QTableWidgetItem()
        item.setText(ex_str.strip_html_and_bracket_markup(text))
        return item

    def _update_results_table(self) -> None:
        self.results_table.setRowCount(0)

        for i, note in enumerate(self.matched_notes):
            self.results_table.insertRow(i)

            # Create type column
            self.results_table.setItem(i, 0, QTableWidgetItem(self._get_note_type_display(note)))
            self.results_table.item(i, 0).setData(Qt.ItemDataRole.UserRole, note.get_id())

            self.results_table.setItem(i, 1, self._create_item(note.get_question()))
            self.results_table.setItem(i, 2, self._create_item(note.get_answer()))

    @staticmethod
    def _get_note_type_display(note: JPNote) -> str:
        """Get a display name for the note type"""
        if isinstance(note, VocabNote):
            return "Vocab"
        if isinstance(note, KanjiNote):
            return "Kanji"
        if isinstance(note, SentenceNote):
            return "Sentence"
        return "Note"

    def on_selection_changed(self) -> None:
        """Handle selection changes (via keyboard or mouse clicks)"""
        selected_rows = self.results_table.selectedItems()
        if not selected_rows:
            return

        # Get the row of the first selected item
        row = selected_rows[0].row()
        self.open_note_at_row(row)

    def on_cell_double_clicked(self, row: int, _column: int) -> None:
        """Handle double-clicking on a cell"""
        self.open_note_at_row(row)
        # No longer closing the dialog with self.accept()

    def open_note_at_row(self, row: int) -> None:
        """Open the note at the specified row"""
        note_id = self.results_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        if note_id:
            from ankiutils import query_builder, search_executor
            search_executor.do_lookup_and_show_previewer(query_builder.open_note_by_id(note_id))

    @classmethod
    def show_dialog(cls, parent: Optional[QWidget] = None) -> None:
        """Show the note search dialog"""
        dialog = cls(parent)
        dialog.exec()
