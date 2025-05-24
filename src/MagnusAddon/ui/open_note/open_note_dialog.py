from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Callable, Optional

from ankiutils import app
from note.kanjinote import KanjiNote
from note.sentences.sentencenote import SentenceNote
from note.vocabulary.vocabnote import VocabNote
from PyQt6.QtCore import Qt, QTimer, pyqtBoundSignal
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from sysutils import ex_str, typed

if TYPE_CHECKING:
    from note.jpnote import JPNote

class NoteSearchDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Find Notes")
        self.resize(1000, 600)

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

        # Create results list
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        # Setup delayed searching (for real-time results as user types)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(200)  # 300ms delay
        typed.checked_cast(pyqtBoundSignal, self.search_timer.timeout).connect(self.perform_search)

        # Connect signals
        typed.checked_cast(pyqtBoundSignal, self.search_input.textChanged).connect(self.on_search_text_changed)
        typed.checked_cast(pyqtBoundSignal, self.results_list.itemDoubleClicked).connect(self.on_item_double_clicked)

        # Initialize the UI
        self.search_input.setFocus()

    def on_search_text_changed(self, text: str) -> None:
        if self.search_timer.isActive():
            self.search_timer.stop()
        self.search_timer.start()

    def perform_search(self) -> None:
        with self._lock:
            """Perform the actual search and update the results list"""
            search_text = self.search_input.text().strip().lower()
            if not search_text:
                self.results_list.clear()
                self.matched_notes = []
                return

            # Get the JP collection
            collection = app.col()
            matching_notes: list[JPNote] = []

            max_notes = 30

            # Search in kanji notes
            matching_notes.extend(self._search_in_notes(
                max_notes - len(matching_notes),
                collection.kanji.all(),
                search_text,
                lambda note: note.get_question().lower(),
                lambda note: note.get_answer().lower(),
                lambda note: " ".join(note.get_readings_clean()).lower() if isinstance(note, KanjiNote) else ""
            ))

            # Search in vocab notes
            matching_notes.extend(self._search_in_notes(
                max_notes - len(matching_notes),
                collection.vocab.all(),
                search_text,
                lambda note: note.get_question().lower(),
                lambda note: note.get_answer().lower(),
                lambda note: ", ".join(note.forms.all_set()).lower() if isinstance(note, VocabNote) else ""
            ))

            # Search in sentence notes
            matching_notes.extend(self._search_in_notes(
                max_notes - len(matching_notes),
                collection.sentences.all(),
                search_text,
                lambda note: note.get_question().lower(),
                lambda note: note.get_answer().lower()
            ))

            self.matched_notes = matching_notes
            self._update_results_list()

    @staticmethod
    def _search_in_notes(max_notes: int, notes: list[JPNote], search_text: str, *extractors: Callable[[JPNote], str]) -> list[JPNote]:
        matches: list[JPNote] = []

        if max_notes <= 0:
            return []

        clean_search = ex_str.strip_html_and_bracket_markup(search_text)

        for note in notes:
            for extractor in extractors:
                try:
                    field_text = extractor(note)
                    clean_field = ex_str.strip_html_and_bracket_markup(field_text)
                    if clean_search in clean_field:
                        matches.append(note)
                        if len(matches) >= max_notes:
                            return matches
                        break
                except:
                    # Skip errors in extraction
                    continue

        return matches

    def _update_results_list(self) -> None:
        self.results_list.clear()

        for note in self.matched_notes:
            # Create a display string for the note
            note_type = self._get_note_type_display(note)
            question = ex_str.strip_html_and_bracket_markup(note.get_question())
            answer = ex_str.strip_html_and_bracket_markup(note.get_answer())

            display_text = f"{note_type}: {question} - {answer}"

            # Create and add the list item
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, note.get_id())
            self.results_list.addItem(item)

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

    def on_item_double_clicked(self, item: QListWidgetItem) -> None:
        note_id = item.data(Qt.ItemDataRole.UserRole)
        if note_id:
            from ankiutils import query_builder, search_executor
            search_executor.do_lookup_and_show_previewer(query_builder.open_note_by_id(note_id))

        self.accept()

    @classmethod
    def show_dialog(cls, parent: Optional[QWidget] = None) -> None:
        """Show the note search dialog"""
        dialog = cls(parent)
        dialog.exec()
