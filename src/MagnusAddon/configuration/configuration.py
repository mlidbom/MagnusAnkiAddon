from typing import Optional

from aqt.qt import *
from ankiutils import app
from configuration.configuration_value import *

class JapaneseConfig:
    def __init__(self) -> None:
        self.selected_option = ConfigurationValueStr("selected_option", "Select Option", "Option 1")
        self.number_value = ConfigurationValueInt("number_value", "Number Value", 5)
        self.yomitan_integration_copy_answer_to_clipboard = ConfigurationValueBool("yomitan_integration_copy_answer_to_clipboard", "Yomitan integration: Copy reviewer answer to clipboard", False)

class JapaneseOptionsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config = app.config

        self.setWindowTitle("Japanese Options")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        # Dropdown
        dropdown_group = QGroupBox(self.config.selected_option.title)
        dropdown_layout = QVBoxLayout()
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Option 1", "Option 2", "Option 3"])
        self.dropdown.setCurrentText(self.config.selected_option.get_value())
        qconnect(self.dropdown.currentTextChanged, self.config.selected_option.set_value)
        dropdown_layout.addWidget(self.dropdown)
        dropdown_group.setLayout(dropdown_layout)
        layout.addWidget(dropdown_group)

        # Number input
        number_group = QGroupBox(self.config.number_value.title)
        number_layout = QVBoxLayout()
        self.number_input = QSpinBox()
        self.number_input.setRange(0, 100)
        self.number_input.setValue(self.config.number_value.get_value())
        qconnect(self.number_input.valueChanged, self.config.number_value.set_value)
        number_layout.addWidget(self.number_input)
        number_group.setLayout(number_layout)
        layout.addWidget(number_group)

        # Checkbox
        checkbox_group = QGroupBox("Feature toggles")
        checkbox_layout = QVBoxLayout()
        self.checkbox = QCheckBox(self.config.yomitan_integration_copy_answer_to_clipboard.title)
        self.checkbox.setChecked(self.config.yomitan_integration_copy_answer_to_clipboard.get_value())
        qconnect(self.checkbox.toggled, self.config.yomitan_integration_copy_answer_to_clipboard.set_value)
        checkbox_layout.addWidget(self.checkbox)
        checkbox_group.setLayout(checkbox_layout)
        layout.addWidget(checkbox_group)


        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        qconnect(self.button_box.clicked, self.accept)
        layout.addWidget(self.button_box)

        self.setLayout(layout)


def show_japanese_options() -> None:
    JapaneseOptionsDialog(mw).exec()