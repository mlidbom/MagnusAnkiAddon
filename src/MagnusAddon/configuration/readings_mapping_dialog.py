from aqt.qt import *

from ankiutils import app
from typing import Optional

from sysutils.ex_str import newline
from sysutils.typed import non_optional

class ReadingsOptionsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config = app.config()

        # for some reason the dead code detector breaks some logic in pycharm here. This method is just fine
        # noinspection PyUnresolvedReferences
        self.setWindowTitle("Readings Mappings")
        self.setMinimumWidth(500)

        mappings_text = newline + self.config.readings_mappings.get_value()

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
        if not text:
            return

        document = non_optional(self.text_edit.document())

        def reset_cursor_to_start() -> None:
            cursor_ = self.text_edit.textCursor()
            cursor_.movePosition(QTextCursor.MoveOperation.Start)
            self.text_edit.setTextCursor(cursor_)

        def remove_higlighting() -> None:
            format_ = QTextCharFormat()
            cursor_ = QTextCursor(document)
            cursor_.select(QTextCursor.SelectionType.Document)
            cursor_.setCharFormat(format_)

        def highlight_block(block:QTextBlock) -> None:
            cursor = QTextCursor(block)
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

                five_lines_height = self.text_edit.fontMetrics().height() * 5
                scrollbar.setValue(scrollbar_position_with_cursor_at_top - five_lines_height)

        reset_cursor_to_start()
        remove_higlighting()

        found = False
        for block_num in range(document.blockCount()):
            block = document.findBlockByNumber(block_num)
            line_text = block.text().strip()

            if line_text.startswith(text):
                highlight_block(block)

                scroll_cursor_to_top()
                found = True
                break

        if not found:
            reset_cursor_to_start()

    def center_on_screen(self) -> None:
        available = non_optional(self.screen()).availableGeometry()
        self.setGeometry(available.x() + (available.width() - self.width()),
                         available.y() + 30,
                         self.width(),
                         available.height() - 60)

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

        self.config.readings_mappings.set_value(sorted_value_lines_without_duplicates_or_blank_lines())
        self.accept()

        from ankiutils import app
        app.ui_utils().refresh()

def show_readings_mappings() -> None:
    from aqt import mw
    dialog = ReadingsOptionsDialog(mw)
    dialog.exec()