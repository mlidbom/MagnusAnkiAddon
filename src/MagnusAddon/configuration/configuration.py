from aqt.qt import *
from ankiutils import app
from configuration.configuration_value import *
from typing import Optional

class JapaneseOptionsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config = app.config()

        self.setWindowTitle("Japanese Options")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        def add_number_spinner_value(grid: QGridLayout, row: int, config_value: ConfigurationValueInt) -> None:
            label = QLabel(config_value.title)
            grid.addWidget(label, row, 0)

            number_input = QSpinBox()
            number_input.setRange(0, 99999)
            number_input.setValue(config_value.get_value())
            qconnect(number_input.valueChanged, config_value.set_value)
            grid.addWidget(number_input, row, 1)

        failed_card_group = QGroupBox("Decrease failed card intervals")
        failed_card_layout = QGridLayout()
        failed_card_layout.setColumnStretch(0, 1)  # Make the label column expandable
        failed_card_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

        add_number_spinner_value(failed_card_layout, 0, self.config.decrease_failed_card_intervals_interval)

        failed_card_group.setLayout(failed_card_layout)
        layout.addWidget(failed_card_group)

        number_group = QGroupBox("Timeboxes")
        number_layout = QGridLayout()
        number_layout.setColumnStretch(0, 1)  # Make the label column expandable
        number_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

        add_number_spinner_value(number_layout, 0, self.config.timebox_sentence_read)
        add_number_spinner_value(number_layout, 1, self.config.timebox_sentence_listen)
        add_number_spinner_value(number_layout, 2, self.config.timebox_vocab_read)
        add_number_spinner_value(number_layout, 3, self.config.timebox_vocab_listen)
        add_number_spinner_value(number_layout, 4, self.config.timebox_kanji_read)

        number_group.setLayout(number_layout)
        layout.addWidget(number_group)

        # checkbox_group = QGroupBox("Feature toggles")
        # checkbox_layout = QVBoxLayout()
        # self.checkbox = QCheckBox(self.config.yomitan_integration_copy_answer_to_clipboard.title)
        # self.checkbox.setChecked(self.config.yomitan_integration_copy_answer_to_clipboard.get_value())
        # qconnect(self.checkbox.toggled, self.config.yomitan_integration_copy_answer_to_clipboard.set_value)
        # checkbox_layout.addWidget(self.checkbox)
        # checkbox_group.setLayout(checkbox_layout)
        # layout.addWidget(checkbox_group)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        qconnect(self.button_box.clicked, self.accept)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

def show_japanese_options() -> None:
    from aqt import mw
    JapaneseOptionsDialog(mw).exec()
