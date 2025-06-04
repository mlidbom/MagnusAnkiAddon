from __future__ import annotations

from ankiutils import app
from aqt import qconnect
from PyQt6.QtGui import QColor, QKeySequence, QShortcut, QTextBlock, QTextCharFormat, QTextCursor
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget
from sysutils.ex_str import newline
from sysutils.typed import checked_cast, non_optional


class ReadingsOptionsDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.config = app.config()

        # for some reason the dead code detector breaks some logic in pycharm here. This method is just fine
        # noinspection PyUnresolvedReferences
        self.setWindowTitle("Readings Mappings")
        self.setMinimumWidth(500)

        mappings_text = newline + self.config.read_readings_mappings_file()

        # Create search field
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText("Type to search...")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)

        # Connect search field to search function
        qconnect(self.search_edit.textChanged, self.search_text)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(mappings_text)

        window_layout = QVBoxLayout()
        window_layout.addLayout(search_layout)
        window_layout.addWidget(self.text_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        shortcut = "Alt+Return"
        self.button_box.setToolTip(f"Save ({shortcut})")
        save_shortcut = QShortcut(QKeySequence(shortcut), self)
        qconnect(save_shortcut.activated, self.save)
        qconnect(self.button_box.clicked, self.save)
        window_layout.addWidget(self.button_box)
        self.setLayout(window_layout)

        self.center_on_screen()

    def search_text(self, text: str) -> None:
        """Search for lines beginning with the search text and scroll to first match."""

        def reset_cursor_to_start() -> None:
            cursor_ = self.text_edit.textCursor()
            cursor_.movePosition(QTextCursor.MoveOperation.Start)
            self.text_edit.setTextCursor(cursor_)

        def remove_higlighting() -> None:
            format_ = QTextCharFormat()
            cursor_ = QTextCursor(document)
            cursor_.select(QTextCursor.SelectionType.Document)
            cursor_.setCharFormat(format_)

        def highlight_block(block_to_highlight:QTextBlock) -> None:
            cursor = QTextCursor(block_to_highlight)
            self.text_edit.setTextCursor(cursor)
            highlight_format = QTextCharFormat()
            highlight_format.setBackground(QColor(255, 255, 0, 70))  # Light yellow highlight
            cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
            cursor.setCharFormat(highlight_format)

        def scroll_cursor_to_top() -> None:
            scrollbar = self.text_edit.verticalScrollBar()
            if scrollbar:
                scrollbar.setValue(scrollbar.maximum())
                self.text_edit.ensureCursorVisible()
                scrollbar_position_with_cursor_at_top = scrollbar.value()

                if scrollbar_position_with_cursor_at_top != scrollbar.maximum():
                    five_lines_height = self.text_edit.fontMetrics().height() * 5
                    scrollbar.setValue(scrollbar_position_with_cursor_at_top - five_lines_height)

        def find_block_starting_with_text() -> QTextBlock | None:
            for block_num_ in range(document.blockCount()):
                block_ = document.findBlockByNumber(block_num_)
                line_text_ = block_.text().strip()

                if line_text_.startswith(text):
                    return block_
            return None

        def find_block_containing_text() -> QTextBlock | None:
            for block_num_ in range(document.blockCount()):
                block_ = document.findBlockByNumber(block_num_)
                line_text_ = block_.text().strip()

                if text in line_text_:
                    return block_
            return None

        document = non_optional(self.text_edit.document())

        reset_cursor_to_start()
        remove_higlighting()
        block_starting_with_text = find_block_starting_with_text()
        if block_starting_with_text:
            highlight_block(block_starting_with_text)
            scroll_cursor_to_top()
            return

        block_containing_text = find_block_containing_text()
        if block_containing_text:
            highlight_block(block_containing_text)
            scroll_cursor_to_top()
            return

    def center_on_screen(self) -> None:
        available = non_optional(self.screen()).availableGeometry()
        self.setGeometry(available.x() + (available.width() - self.width()),
                         available.y() + 30,
                         self.width(),
                         300)

    def save(self) -> None:
        def sorted_value_lines_without_duplicates_or_blank_lines() -> str:
            lines = self.text_edit.toPlainText().splitlines()
            lines.reverse() #the top latest lines are now the last lines and will overwrite earlier lines

            readings_mappings = {
                line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip()
                for line in lines
                if ":" in line
            }

            new_lines = [f"{line[0]}:{line[1]}" for line in readings_mappings.items()]

            return "\n".join(sorted(new_lines))

        self.config.save_mappings(sorted_value_lines_without_duplicates_or_blank_lines())
        self.accept()

        app.get_ui_utils().refresh()

def show_readings_mappings() -> None:
    from aqt import mw
    dialog = ReadingsOptionsDialog(checked_cast(QWidget, mw))
    dialog.exec()