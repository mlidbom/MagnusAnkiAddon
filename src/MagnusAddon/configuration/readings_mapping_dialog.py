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

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(mappings_text)

        window_layout = QVBoxLayout()
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