from __future__ import annotations

import threading
from typing import TYPE_CHECKING, cast, final

from anki.notes import NoteId
from jaslib.sysutils import ex_str, kana_utils, typed
from jaslib.sysutils.typed import non_optional
from jastudio.ankiutils.app import col
from jastudio.note.jpnote import JPNote
from jastudio.note.kanjinote import KanjiNote
from jastudio.note.sentences.sentencenote import SentenceNote
from jastudio.note.vocabulary.vocabnote import VocabNote
from PyQt6.QtCore import Qt, pyqtBoundSignal
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QProgressBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from collections.abc import Callable


@final
class NoteSearchDialog(QDialog): # Cannot inherit Slots for some QT internal reason
    # Singleton instance
    _instance: NoteSearchDialog | None = None

    @classmethod
    def instance(cls) -> NoteSearchDialog:
        """Access to the singleton instance, creating it if needed."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Find Notes")
        self.resize(1800, 1100)

        # Set the window to be always on top but not modal
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.matched_notes: list[JPNote] = []
        self._lock = threading.Lock()
        self._max_results = 100  # Maximum number of results to show

        # Rest of the initialization code...

        layout = QVBoxLayout(self)

        # Create search input field
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Separate multiple conditions with &&  r:readings-only-condition, a:answer-only-condition, q:question-only-condition")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Create status and progress indicator area right below search
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Hit enter to search")
        self.status_label.setMinimumHeight(25)  # Give it some height to prevent layout shifting

        # Create progress bar for busy indicator
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate mode
        self.progress_bar.setMinimumHeight(20)  # Make it a bit taller
        self.progress_bar.hide()  # Hidden by default

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar, 1)  # 1 = stretch factor to take up available space
        layout.addLayout(status_layout)

        # Create results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Type", "Question", "Answer"])  # pyright: ignore[reportUnknownMemberType]
        non_optional(self.results_table.horizontalHeader()).setSectionResizeMode(QHeaderView.ResizeMode.Interactive)  # Make all columns resizable
        self.results_table.setColumnWidth(1, 200)  # Set Question column width to 200 pixels
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.results_table)

        # Connect signals
        typed.checked_cast(pyqtBoundSignal, self.search_input.returnPressed).connect(self.perform_search)  # pyright: ignore[reportUnknownMemberType]
        typed.checked_cast(pyqtBoundSignal, self.results_table.cellDoubleClicked).connect(self.on_cell_double_clicked)  # pyright: ignore[reportUnknownMemberType]
        # Add selection change signal to handle keyboard/mouse selection
        typed.checked_cast(pyqtBoundSignal, self.results_table.itemSelectionChanged).connect(self.on_selection_changed)  # pyright: ignore[reportUnknownMemberType]

        self.search_input.setFocus()

    def perform_search(self) -> None:
        with self._lock:
            """Perform the actual search and update the results table"""
            search_text = self.search_input.text().strip()
            if not search_text:
                self.results_table.setRowCount(0)
                self.matched_notes = []
                return

            # Show the busy indicator
            self.status_label.setText("Searching...")
            self.progress_bar.show()

            # Process events to ensure UI updates
            from PyQt6.QtWidgets import QApplication
            QApplication.processEvents()

            try:
                # Get the JP collection
                matching_notes: list[JPNote] = []

                def kanji_readings(note: KanjiNote) -> str:
                    return " ".join(note.get_readings_clean())

                def vocab_readings(vocab: VocabNote) -> str:
                    return " ".join(vocab.readings.get())

                def vocab_romaji_readings(vocab: VocabNote) -> str:
                    return kana_utils.romanize(vocab_readings(vocab))

                def vocab_forms(vocab: VocabNote) -> str:
                    return " ".join(vocab.forms.without_noise_characters())

                def question_length(note: JPNote) -> int:
                    return len(note.get_question())

                def kanji_romaji_readings(note: KanjiNote) -> str:
                    return note.get_romaji_readings()

                def note_question(note_: JPNote) -> str:
                    return ex_str.strip_html_and_bracket_markup(note_.get_question())

                def note_answer(note_: JPNote) -> str:
                    return ex_str.strip_html_and_bracket_markup(note_.get_answer())

                # Search in kanji notes
                matching_notes.extend(self._search_in_notes(
                    self._max_results - len(matching_notes),
                    col().kanji.all(),
                    search_text,
                    kanji_readings=kanji_readings,
                    kanji_romaji_readings=kanji_romaji_readings,
                    question=note_question,
                    answer=note_answer
                ))

                # Search in vocab notes
                matching_notes.extend(self._search_in_notes(
                    self._max_results - len(matching_notes),
                    sorted(col().vocab.all(), key=question_length),
                    search_text,
                    vocab_readings=vocab_readings,
                    vocab_romaji_readings=vocab_romaji_readings,
                    forms=vocab_forms,
                    question=note_question,
                    answer=note_answer
                ))

                # Search in sentence notes
                matching_notes.extend(self._search_in_notes(
                    self._max_results - len(matching_notes),
                    sorted(col().sentences.all(), key=question_length),
                    search_text,
                    question=note_question,
                    answer=note_answer
                ))

                self.matched_notes = matching_notes
                self._update_results_table()

                # Update status with result count
                result_count = len(matching_notes)
                if result_count == 0:
                    self.status_label.setText("No results found")
                elif result_count >= self._max_results:
                    self.status_label.setText(f"{self._max_results}+ notes found. Showing first {self._max_results}")
                else:
                    self.status_label.setText(f"{result_count} note{'s' if result_count != 1 else ''} found")

            finally:
                # Hide the busy indicator
                self.progress_bar.hide()


    @classmethod
    def _search_in_notes[TNote: JPNote](cls, max_notes: int, notes: list[TNote], search_text: str, **extractors: Callable[[TNote], str]) -> list[JPNote]:
        matches: list[JPNote] = []

        if max_notes <= 0:
            return []

        # Split search text by " && " to get multiple conditions
        search_conditions = [condition.strip() for condition in search_text.split(" && ")]

        for note in notes:
            all_conditions_match = True

            for condition in search_conditions:
                condition_matches = False
                condition_lower = condition.lower()

                # Check for prefixed search
                if condition.startswith("r:"):
                    # Only search in reading fields
                    reading_value = condition[2:].strip().lower()
                    reading_fields = {extractor_name: extractor for extractor_name, extractor in extractors.items() if "reading" in extractor_name.lower()}

                    if not reading_fields:
                        # Skip this note type if it doesn't have reading fields
                        all_conditions_match = False
                        break

                    for extractor in reading_fields.values():
                        field_text = extractor(note)
                        clean_field = ex_str.strip_html_and_bracket_markup(field_text).lower()
                        if reading_value in clean_field:
                            condition_matches = True
                            break
                elif condition.startswith("a:"):
                    # Only search in answer field
                    answer_value = condition[2:].strip().lower()
                    if "answer" in extractors:
                        field_text = extractors["answer"](note)
                        clean_field = ex_str.strip_html_and_bracket_markup(field_text).lower()
                        if answer_value in clean_field:
                            condition_matches = True
                elif condition.startswith("q:"):
                    # Only search in question field
                    question_value = condition[2:].strip().lower()
                    if "question" in extractors:
                        field_text = extractors["question"](note)
                        clean_field = ex_str.strip_html_and_bracket_markup(field_text).lower()
                        if question_value in clean_field:
                            condition_matches = True
                else:
                    # Standard search in all fields
                    for extractor in extractors.values():
                        field_text = extractor(note)
                        clean_field = ex_str.strip_html_and_bracket_markup(field_text).lower()
                        if condition_lower in clean_field:
                            condition_matches = True
                            break

                if not condition_matches:
                    all_conditions_match = False
                    break

            if all_conditions_match:
                matches.append(note)
                if len(matches) >= max_notes:
                    return matches

        return matches

    @classmethod
    def _create_item(cls, text: str, is_question: bool = False) -> QTableWidgetItem:
        item = QTableWidgetItem()
        item.setText(ex_str.strip_html_and_bracket_markup(text))

        # Apply special formatting to question column
        if is_question:
            font = item.font()
            font.setFamily("Meiryo UI")
            font.setPointSize(int(font.pointSize() * 1.5))  # Increase font size by 50%
            item.setFont(font)

        return item

    def _update_results_table(self) -> None:
        self.results_table.setRowCount(0)

        for i, note in enumerate(self.matched_notes):
            self.results_table.insertRow(i)

            # Create type column
            self.results_table.setItem(i, 0, QTableWidgetItem(self._get_note_type_display(note)))
            non_optional(self.results_table.item(i, 0)).setData(Qt.ItemDataRole.UserRole, note.get_id())

            self.results_table.setItem(i, 1, self._create_item(note.get_question(), is_question=True))
            self.results_table.setItem(i, 2, self._create_item(note.get_answer()))

        self.results_table.resizeColumnsToContents()

    @classmethod
    def _get_note_type_display(cls, note: JPNote) -> str:
        """Get a display name for the note type"""
        if isinstance(note, VocabNote):
            return "Vocab"
        if isinstance(note, KanjiNote):
            return "Kanji"
        if isinstance(note, SentenceNote):
            return "Sentence"
        return "Note"

    def on_selection_changed(self) -> None:
        selected_rows = self.results_table.selectedItems()
        if not selected_rows:
            return

        self.open_notes_at_rows({item.row() for item in selected_rows})

    def on_cell_double_clicked(self, row: int, _column: int) -> None:
        self.open_notes_at_rows({row})

    def open_notes_at_rows(self, rows: set[int]) -> None:
        note_ids = []
        for row in rows:
            note_id = cast(NoteId, non_optional(self.results_table.item(row, 0)).data(Qt.ItemDataRole.UserRole))
            if note_id:
                note_ids.append(note_id)  # pyright: ignore[reportUnknownMemberType]

        if note_ids:
            from jastudio.ankiutils import query_builder, search_executor
            search_executor.do_lookup_and_show_previewer(query_builder.notes_by_id(note_ids))  # pyright: ignore[reportUnknownArgumentType]
            self.instance().activateWindow()  # the search will lose our focus, reactivate it

    @classmethod
    def toggle_dialog_visibility(cls) -> None:
        if cls.instance().isVisible():
            cls.instance().hide()
            return

        cls.instance().show()
        cls.instance().raise_()
        cls.instance().activateWindow()
        cls.instance().search_input.setFocus()
