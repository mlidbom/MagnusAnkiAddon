from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Optional

from aqt.utils import openLink
from language_services.english_dictionary import english_dict_search
from PyQt6.QtCore import Qt, pyqtBoundSignal
from PyQt6.QtWidgets import QApplication, QDialog, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from sysutils import typed

if TYPE_CHECKING:
    from language_services.english_dictionary.english_dict_search import EnglishWord

class EnglishWordSearchDialog(QDialog):
    # Singleton instance
    _instance: Optional[EnglishWordSearchDialog] = None

    @classmethod
    def instance(cls) -> EnglishWordSearchDialog:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Find English Words")
        self.resize(800, 600)

        # Set the window to be always on top but not modal
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self._lock = threading.Lock()
        self._max_results = 100  # Maximum number of results to show

        layout = QVBoxLayout(self)

        # Create search input field
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter the beginning of an English word")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Create results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)  # Two columns: word and definition
        self.results_table.setHorizontalHeaderLabels(["Word", "Definition"])
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Configure column widths
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.results_table)

        typed.checked_cast(pyqtBoundSignal, self.search_input.textChanged).connect(self.perform_search)
        typed.checked_cast(pyqtBoundSignal, self.results_table.cellDoubleClicked).connect(self.on_cell_double_clicked)

        self.search_input.setFocus()

    def perform_search(self) -> None:
        with self._lock:
            search_text = self.search_input.text().strip()
            if not search_text:
                self.results_table.setRowCount(0)
                return

            matching_words: list[EnglishWord] = english_dict_search.dictionary().words_containing_starting_with_first_then_by_shortest_first(search_text)
            matching_words = matching_words[:self._max_results]

            self._update_results_table(matching_words)

    def _update_results_table(self, words: list[english_dict_search.EnglishWord]) -> None:
        self.results_table.setRowCount(0)  # Clear the table
        self.results_table.setRowCount(len(words))

        for row, word in enumerate(words):
            # Word item
            word_item = QTableWidgetItem(word.word)
            word_item.setData(Qt.ItemDataRole.UserRole, word.word)  # Store the word for double-click
            self.results_table.setItem(row, 0, word_item)

            # Definition item
            definition_item = QTableWidgetItem(word.senses[0].definition)
            self.results_table.setItem(row, 1, definition_item)

    def on_cell_double_clicked(self, row: int, _column: int) -> None:
        word_item = self.results_table.item(row, 0)
        if word_item:
            selected_word = word_item.data(Qt.ItemDataRole.UserRole)
            if selected_word:
                if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier:
                    openLink(f"https://www.merriam-webster.com/dictionary/{selected_word}")
                elif QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier:
                    openLink(f"https://www.google.com/search?q=define+{selected_word}")
                else:
                    openLink(f"https://www.oed.com/search/dictionary/?scope=Entries&q={selected_word}")

    @classmethod
    def toggle_dialog_visibility(cls) -> None:
        if cls.instance().isVisible():
            cls.instance().hide()
            return

        cls.instance().show()
        cls.instance().raise_()
        cls.instance().activateWindow()
        cls.instance().search_input.setFocus()
