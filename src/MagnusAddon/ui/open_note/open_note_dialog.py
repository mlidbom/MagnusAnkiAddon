from __future__ import annotations

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
        self.resize(600, 400)

        # Track the matched notes
        self.matched_notes: list[JPNote] = []

        # Create layout
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
        self.search_timer.setInterval(300)  # 300ms delay
        typed.checked_cast(pyqtBoundSignal, self.search_timer.timeout).connect(self.perform_search)

        # Connect signals
        typed.checked_cast(pyqtBoundSignal, self.search_input.textChanged).connect(self.on_search_text_changed)
        typed.checked_cast(pyqtBoundSignal, self.results_list.itemDoubleClicked).connect(self.on_item_double_clicked)

        # Initialize the UI
        self.search_input.setFocus()

    def on_search_text_changed(self, text: str) -> None:
        """Start the search timer whenever the text changes"""
        self.search_timer.start()

    def perform_search(self) -> None:
        """Perform the actual search and update the results list"""
        search_text = self.search_input.text().strip().lower()
        if not search_text:
            self.results_list.clear()
            self.matched_notes = []
            return

        # Get the JP collection
        collection = app.col()
        all_notes: list[JPNote] = []

        # Search in vocab notes
        all_notes.extend(self._search_in_notes(
            collection.vocab.all(),
            search_text,
            lambda note: note.get_question().lower(),
            lambda note: note.get_answer().lower(),
            lambda note: ", ".join(note.forms.all_set()).lower() if isinstance(note, VocabNote) else ""
        ))

        # Search in kanji notes
        all_notes.extend(self._search_in_notes(
            collection.kanji.all(),
            search_text,
            lambda note: note.get_question().lower(),
            lambda note: note.get_answer().lower(),
            lambda note: " ".join(note.get_readings_clean()).lower() if isinstance(note, KanjiNote) else ""
        ))

        # Search in sentence notes
        all_notes.extend(self._search_in_notes(
            collection.sentences.all(),
            search_text,
            lambda note: note.get_question().lower(),
            lambda note: note.get_answer().lower()
        ))

        # Update the matched notes and display them
        self.matched_notes = all_notes
        self._update_results_list()

    def _search_in_notes(self, notes: list[JPNote], search_text: str, *extractors: Callable[[JPNote], str]) -> list[JPNote]:
        """Search in a collection of notes using multiple field extractors"""
        matches: list[JPNote] = []

        # Clean the search text for more accurate matching
        clean_search = ex_str.strip_html_and_bracket_markup(search_text)

        for note in notes:
            for extractor in extractors:
                try:
                    field_text = extractor(note)
                    clean_field = ex_str.strip_html_and_bracket_markup(field_text)
                    if clean_search in clean_field:
                        matches.append(note)
                        break
                except:
                    # Skip errors in extraction
                    continue

        return matches

    def _update_results_list(self) -> None:
        """Update the UI with search results"""
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

    def _get_note_type_display(self, note: JPNote) -> str:
        """Get a display name for the note type"""
        if isinstance(note, VocabNote):
            return "Vocab"
        if isinstance(note, KanjiNote):
            return "Kanji"
        if isinstance(note, SentenceNote):
            return "Sentence"
        return "Note"

    def on_item_double_clicked(self, item: QListWidgetItem) -> None:
        """Handle double-click on a result item"""
        item.data(Qt.ItemDataRole.UserRole)
        # For now, we'll just close the dialog
        # In a future implementation, this is where you'd open the note
        self.accept()

    @classmethod
    def show_dialog(cls, parent: Optional[QWidget] = None) -> None:
        """Show the note search dialog"""
        dialog = cls(parent)
        dialog.exec()