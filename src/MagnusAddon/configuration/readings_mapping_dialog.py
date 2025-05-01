from aqt.qt import *
from pkg_resources import non_empty_lines

from ankiutils import app
from typing import Optional

class ReadingsOptionsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config = app.config()

        # for some reason the dead code detector breaks some logic in pycharm here. This method is just fine
        # noinspection PyUnresolvedReferences
        self.setWindowTitle("Readings Mappings")
        self.setMinimumWidth(800)

        mappings_text = self.config.readings_mappings.get_value()

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(mappings_text)

        window_layout = QVBoxLayout()
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        qconnect(self.button_box.clicked, self.save)
        window_layout.addWidget(self.text_edit)
        window_layout.addWidget(self.button_box)
        self.setLayout(window_layout)

    def save(self) -> None:
        def sorted_value_lines_without_blank_lines() -> str:
            return "\n".join([line for line in (sorted(self.text_edit.toPlainText().splitlines())) if line != ""])

        self.config.readings_mappings.set_value(sorted_value_lines_without_blank_lines())

        self.accept()

def show_readings_mappings() -> None:
    from aqt import mw
    ReadingsOptionsDialog(mw).exec()
