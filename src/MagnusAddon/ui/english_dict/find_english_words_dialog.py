from __future__ import annotations

import threading
from typing import Optional

from language_services.english_dictionary import english_dict_search
from PyQt6.QtCore import Qt, pyqtBoundSignal
from PyQt6.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QProgressBar, QVBoxLayout, QWidget
from sysutils import typed


class EnglishWordSearchDialog(QDialog):
    # Singleton instance
    _instance: Optional[EnglishWordSearchDialog] = None

    @classmethod
    def instance(cls) -> EnglishWordSearchDialog:
        """Access to the singleton instance, creating it if needed."""
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

        # Create results list
        self.results_list = QListWidget()
        self.results_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.results_list)

        # Connect signals
        typed.checked_cast(pyqtBoundSignal, self.search_input.returnPressed).connect(self.perform_search)
        typed.checked_cast(pyqtBoundSignal, self.search_input.textChanged).connect(self.perform_search)
        typed.checked_cast(pyqtBoundSignal, self.results_list.itemDoubleClicked).connect(self.on_item_double_clicked)

        self.search_input.setFocus()

    def perform_search(self) -> None:
        with self._lock:
            """Perform the search and update the results list"""
            search_text = self.search_input.text().strip()
            if not search_text:
                self.results_list.clear()
                return

            # Show the busy indicator
            self.status_label.setText("Searching...")
            self.progress_bar.show()

            # Process events to ensure UI updates
            from PyQt6.QtWidgets import QApplication
            QApplication.processEvents()

            try:
                # Search for words starting with the provided text
                matching_words = english_dict_search.dictionary().words_starting_with_shortest_first(search_text)

                # Limit to max results
                if len(matching_words) > self._max_results:
                    matching_words = matching_words[:self._max_results]

                self._update_results_list(matching_words)

                # Update status with result count
                result_count = len(matching_words)
                if result_count == 0:
                    self.status_label.setText("No results found")
                elif result_count >= self._max_results:
                    self.status_label.setText(f"{self._max_results}+ words found. Showing first {self._max_results}")
                else:
                    self.status_label.setText(f"{result_count} word{'s' if result_count != 1 else ''} found")

            finally:
                # Hide the busy indicator
                self.progress_bar.hide()

    def _update_results_list(self, words: list[english_dict_search.EnglishWord]) -> None:
        self.results_list.clear()

        for word in words:
            item = QListWidgetItem()
            display_text = f"{word.word} ({word.pos}): {word.definition}"
            item.setText(display_text)
            item.setData(Qt.ItemDataRole.UserRole, word.word)
            self.results_list.addItem(item)

    def on_item_double_clicked(self, item: QListWidgetItem) -> None:
        selected_word = item.data(Qt.ItemDataRole.UserRole)
        if selected_word:
            # Here you can implement what happens when a word is double-clicked
            # For example, copying to clipboard or showing detailed information
            QApplication.clipboard().setText(selected_word)
            self.status_label.setText(f"Copied '{selected_word}' to clipboard")

    @classmethod
    def toggle_dialog_visibility(cls) -> None:
        if cls.instance().isVisible():
            cls.instance().hide()
            return

        cls.instance().show()
        cls.instance().raise_()
        cls.instance().activateWindow()
        cls.instance().search_input.setFocus()