from aqt.qt import *

from ankiutils import app
from configuration.configuration_value import *
from typing import Optional
from PyQt6.QtWidgets import QGridLayout, QLabel, QDoubleSpinBox

class JapaneseOptionsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config = app.config()

        # for some reason the dead code detector breaks some logic in pycharm here. This method is just fine
        # noinspection PyUnresolvedReferences
        self.setWindowTitle("Japanese Options")
        self.setMinimumWidth(300)

        window_layout = QVBoxLayout()

        def add_number_spinner_value(grid: QGridLayout, row: int, config_value: ConfigurationValueInt) -> None:
            label = QLabel(config_value.title)
            grid.addWidget(label, row, 0)

            # noinspection PyArgumentList
            number_input = QSpinBox()
            number_input.setRange(0, 99999)
            number_input.setValue(config_value.get_value())
            qconnect(number_input.valueChanged, config_value.set_value)
            grid.addWidget(number_input, row, 1)

        def add_double_spinner_value(grid: QGridLayout, row: int, config_value: ConfigurationValueFloat) -> None:
            label = QLabel(config_value.title)
            grid.addWidget(label, row, 0)

            # Create a QDoubleSpinBox for floating-point input
            double_input = QDoubleSpinBox()
            double_input.setRange(0.0, 100.0)  # Set the range for the floating-point values
            double_input.setDecimals(2)  # Set precision to 2 decimal places
            double_input.setValue(config_value.get_value())  # Set initial value
            double_input.setSingleStep(0.05)  # Set step size for increment/decrement

            # Connect the valueChanged signal to update the config value
            qconnect(double_input.valueChanged, config_value.set_value)

            grid.addWidget(double_input, row, 1)

        def setup_decrease_failed_card_interval_section() -> None:
            failed_card_group = QGroupBox("Decrease failed card intervals")
            # noinspection PyArgumentList
            failed_card_layout = QGridLayout()
            failed_card_layout.setColumnStretch(0, 1)  # Make the label column expandable
            failed_card_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_number_spinner_value(failed_card_layout, 0, self.config.decrease_failed_card_intervals_interval)

            failed_card_group.setLayout(failed_card_layout)
            window_layout.addWidget(failed_card_group)

        def setup_boost_failed_card_allowed_time_section() -> None:
            failed_card_allowed_time_group = QGroupBox("Boost failed card allowed time")
            # noinspection PyArgumentList
            failed_card_allowed_time_layout = QGridLayout()
            failed_card_allowed_time_layout.setColumnStretch(0, 1)  # Make the label column expandable
            failed_card_allowed_time_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_double_spinner_value(failed_card_allowed_time_layout, 0, self.config.boost_failed_card_allowed_time_by_factor)

            failed_card_allowed_time_group.setLayout(failed_card_allowed_time_layout)
            window_layout.addWidget(failed_card_allowed_time_group)

        def setup_vocab_autoadvance_timings() -> None:
            vocab_autoadvance_timings_group = QGroupBox("Vocab autoadvance timings")
            # noinspection PyArgumentList
            vocab_autoadvance_timings_layout = QGridLayout()
            vocab_autoadvance_timings_layout.setColumnStretch(0, 1)  # Make the label column expandable
            vocab_autoadvance_timings_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_double_spinner_value(vocab_autoadvance_timings_layout, 0, self.config.autoadvance_vocab_starting_seconds)
            add_double_spinner_value(vocab_autoadvance_timings_layout, 1, self.config.autoadvance_vocab_hiragana_seconds)
            add_double_spinner_value(vocab_autoadvance_timings_layout, 2, self.config.autoadvance_vocab_katakana_seconds)
            add_double_spinner_value(vocab_autoadvance_timings_layout, 3, self.config.autoadvance_vocab_kanji_seconds)

            vocab_autoadvance_timings_group.setLayout(vocab_autoadvance_timings_layout)
            window_layout.addWidget(vocab_autoadvance_timings_group)

        def setup_sentence_autoadvance_timings() -> None:
            sentence_autoadvance_timings_group = QGroupBox("Sentence autoadvance timings")
            # noinspection PyArgumentList
            sentence_autoadvance_timings_layout = QGridLayout()
            sentence_autoadvance_timings_layout.setColumnStretch(0, 1)  # Make the label column expandable
            sentence_autoadvance_timings_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_double_spinner_value(sentence_autoadvance_timings_layout, 0, self.config.autoadvance_sentence_starting_seconds)
            add_double_spinner_value(sentence_autoadvance_timings_layout, 1, self.config.autoadvance_sentence_hiragana_seconds)
            add_double_spinner_value(sentence_autoadvance_timings_layout, 2, self.config.autoadvance_sentence_katakana_seconds)
            add_double_spinner_value(sentence_autoadvance_timings_layout, 3, self.config.autoadvance_sentence_kanji_seconds)

            sentence_autoadvance_timings_group.setLayout(sentence_autoadvance_timings_layout)
            window_layout.addWidget(sentence_autoadvance_timings_group)

        def setup_timeboxes_section() -> None:
            number_group = QGroupBox("Timeboxes")
            # noinspection PyArgumentList
            number_layout = QGridLayout()
            number_layout.setColumnStretch(0, 1)  # Make the label column expandable
            number_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_number_spinner_value(number_layout, 0, self.config.timebox_sentence_read)
            add_number_spinner_value(number_layout, 1, self.config.timebox_sentence_listen)
            add_number_spinner_value(number_layout, 2, self.config.timebox_vocab_read)
            add_number_spinner_value(number_layout, 3, self.config.timebox_vocab_listen)
            add_number_spinner_value(number_layout, 4, self.config.timebox_kanji_read)

            number_group.setLayout(number_layout)
            window_layout.addWidget(number_group)

        def setup_debounce_section() -> None:
            number_group = QGroupBox("Prevent accidental clicks")
            # noinspection PyArgumentList
            no_accidental_clicks_layout = QGridLayout()
            no_accidental_clicks_layout.setColumnStretch(0, 1)  # Make the label column expandable
            no_accidental_clicks_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_double_spinner_value(no_accidental_clicks_layout, 0, self.config.minimum_time_viewing_question)
            add_double_spinner_value(no_accidental_clicks_layout, 1, self.config.minimum_time_viewing_answer)

            number_group.setLayout(no_accidental_clicks_layout)
            window_layout.addWidget(number_group)

        setup_vocab_autoadvance_timings()
        setup_sentence_autoadvance_timings()
        setup_boost_failed_card_allowed_time_section()
        setup_decrease_failed_card_interval_section()
        setup_timeboxes_section()
        setup_debounce_section()

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
        window_layout.addWidget(self.button_box)

        self.setLayout(window_layout)

def show_japanese_options() -> None:
    from aqt import mw
    JapaneseOptionsDialog(mw).exec()
