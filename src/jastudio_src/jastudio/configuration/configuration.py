from __future__ import annotations

from typing import TYPE_CHECKING

from jaspythonutils.sysutils.typed import checked_cast
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget

from jastudio.ankiutils import app

if TYPE_CHECKING:
    from JAStudio.Core.Configuration import ConfigurationValue_1, JapaneseConfig

class JapaneseOptionsDialog(QDialog): # Cannot inherit Slots for some QT internal reason
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.config: JapaneseConfig = app.config()

        # for some reason the dead code detector breaks some logic in pycharm here. This method is just fine
        # noinspection PyUnresolvedReferences
        self.setWindowTitle("Japanese Options")
        self.setMinimumWidth(600)

        window_layout = QVBoxLayout()
        main_content_layout = QHBoxLayout()

        # Left side - numeric settings
        left_layout = QVBoxLayout()

        # Right side - toggleable settings
        right_layout = QVBoxLayout()

        def add_number_spinner_value(grid: QGridLayout, row: int, config_value: ConfigurationValue_1[int]) -> None:
            label = QLabel(config_value.Title)
            grid.addWidget(label, row, 0)

            # noinspection PyArgumentList
            number_input = QSpinBox()
            number_input.setRange(0, 99999)
            number_input.setValue(config_value.GetValue())
            checked_cast(pyqtBoundSignal, number_input.valueChanged).connect(config_value.SetValue)  # pyright: ignore[reportUnknownMemberType]
            grid.addWidget(number_input, row, 1)

        def add_double_spinner_value(grid: QGridLayout, row: int, config_value: ConfigurationValue_1[float]) -> None:
            label = QLabel(config_value.Title)
            grid.addWidget(label, row, 0)

            # Create a QDoubleSpinBox for floating-point input
            double_input = QDoubleSpinBox()
            double_input.setRange(0.0, 100.0)  # Set the range for the floating-point values
            double_input.setDecimals(2)  # Set precision to 2 decimal places
            double_input.setValue(config_value.GetValue())  # Set initial value
            double_input.setSingleStep(0.05)  # Set step size for increment/decrementb

            # Connect the valueChanged signal to update the config value
            checked_cast(pyqtBoundSignal, double_input.valueChanged).connect(config_value.SetValue)  # pyright: ignore[reportUnknownMemberType]

            grid.addWidget(double_input, row, 1)

        def add_checkbox_value(layout: QVBoxLayout, config_value: ConfigurationValue_1[bool]) -> None:
            checkbox = QCheckBox(config_value.Title)
            checkbox.setChecked(config_value.GetValue())
            checked_cast(pyqtBoundSignal, checkbox.toggled).connect(config_value.SetValue)  # pyright: ignore[reportUnknownMemberType]
            layout.addWidget(checkbox)

        def setup_decrease_failed_card_interval_section() -> None:
            failed_card_group = QGroupBox("Decrease failed card intervals")
            # noinspection PyArgumentList
            failed_card_layout = QGridLayout()
            failed_card_layout.setColumnStretch(0, 1)  # Make the label column expandable
            failed_card_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_number_spinner_value(failed_card_layout, 0, self.config.DecreaseFailedCardIntervalsInterval)

            failed_card_group.setLayout(failed_card_layout)
            left_layout.addWidget(failed_card_group)

        def setup_boost_failed_card_allowed_time_section() -> None:
            failed_card_allowed_time_group = QGroupBox("Boost failed card allowed time")
            # noinspection PyArgumentList
            failed_card_allowed_time_layout = QGridLayout()
            failed_card_allowed_time_layout.setColumnStretch(0, 1)  # Make the label column expandable
            failed_card_allowed_time_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_double_spinner_value(failed_card_allowed_time_layout, 0, self.config.BoostFailedCardAllowedTimeByFactor)

            failed_card_allowed_time_group.setLayout(failed_card_allowed_time_layout)
            left_layout.addWidget(failed_card_allowed_time_group)

        def setup_vocab_autoadvance_timings() -> None:
            vocab_autoadvance_timings_group = QGroupBox("Vocab autoadvance timings")
            # noinspection PyArgumentList
            vocab_autoadvance_timings_layout = QGridLayout()
            vocab_autoadvance_timings_layout.setColumnStretch(0, 1)  # Make the label column expandable
            vocab_autoadvance_timings_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_double_spinner_value(vocab_autoadvance_timings_layout, 0, self.config.AutoadvanceVocabStartingSeconds)
            add_double_spinner_value(vocab_autoadvance_timings_layout, 1, self.config.AutoadvanceVocabHiraganaSeconds)
            add_double_spinner_value(vocab_autoadvance_timings_layout, 2, self.config.AutoadvanceVocabKatakanaSeconds)
            add_double_spinner_value(vocab_autoadvance_timings_layout, 3, self.config.AutoadvanceVocabKanjiSeconds)

            vocab_autoadvance_timings_group.setLayout(vocab_autoadvance_timings_layout)
            left_layout.addWidget(vocab_autoadvance_timings_group)

        def setup_sentence_autoadvance_timings() -> None:
            sentence_autoadvance_timings_group = QGroupBox("Sentence autoadvance timings")
            # noinspection PyArgumentList
            sentence_autoadvance_timings_layout = QGridLayout()
            sentence_autoadvance_timings_layout.setColumnStretch(0, 1)  # Make the label column expandable
            sentence_autoadvance_timings_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_double_spinner_value(sentence_autoadvance_timings_layout, 0, self.config.AutoadvanceSentenceStartingSeconds)
            add_double_spinner_value(sentence_autoadvance_timings_layout, 1, self.config.AutoadvanceSentenceHiraganaSeconds)
            add_double_spinner_value(sentence_autoadvance_timings_layout, 2, self.config.AutoadvanceSentenceKatakanaSeconds)
            add_double_spinner_value(sentence_autoadvance_timings_layout, 3, self.config.AutoadvanceSentenceKanjiSeconds)

            sentence_autoadvance_timings_group.setLayout(sentence_autoadvance_timings_layout)
            left_layout.addWidget(sentence_autoadvance_timings_group)

        def setup_timeboxes_section() -> None:
            number_group = QGroupBox("Timeboxes")
            # noinspection PyArgumentList
            number_layout = QGridLayout()
            number_layout.setColumnStretch(0, 1)  # Make the label column expandable
            number_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_number_spinner_value(number_layout, 0, self.config.TimeboxSentenceRead)
            add_number_spinner_value(number_layout, 1, self.config.TimeboxSentenceListen)
            add_number_spinner_value(number_layout, 2, self.config.TimeboxVocabRead)
            add_number_spinner_value(number_layout, 3, self.config.TimeboxVocabListen)
            add_number_spinner_value(number_layout, 4, self.config.TimeboxKanjiRead)

            number_group.setLayout(number_layout)
            left_layout.addWidget(number_group)

        def setup_debounce_section() -> None:
            number_group = QGroupBox("Prevent accidental clicks")
            # noinspection PyArgumentList
            no_accidental_clicks_layout = QGridLayout()
            no_accidental_clicks_layout.setColumnStretch(0, 1)  # Make the label column expandable
            no_accidental_clicks_layout.setColumnStretch(1, 0)  # Keep the spinner column fixed width

            add_double_spinner_value(no_accidental_clicks_layout, 0, self.config.MinimumTimeViewingQuestion)
            add_double_spinner_value(no_accidental_clicks_layout, 1, self.config.MinimumTimeViewingAnswer)

            number_group.setLayout(no_accidental_clicks_layout)
            left_layout.addWidget(number_group)

        def setup_feature_toggles_section() -> None:
            for toggle_section in self.config.FeatureToggles:
                section_name = toggle_section.Item1
                toggles = toggle_section.Item2
                toggles_group = QGroupBox(section_name)
                toggles_layout = QVBoxLayout()

                for toggle in toggles:
                    add_checkbox_value(toggles_layout, toggle)

                toggles_group.setLayout(toggles_layout)
                right_layout.addWidget(toggles_group)

        setup_vocab_autoadvance_timings()
        setup_sentence_autoadvance_timings()
        setup_boost_failed_card_allowed_time_section()
        setup_decrease_failed_card_interval_section()
        setup_timeboxes_section()
        setup_debounce_section()

        setup_feature_toggles_section()

        # Add left and right layouts to main content layout
        main_content_layout.addLayout(left_layout)
        main_content_layout.addLayout(right_layout)

        # Add main content to window layout
        window_layout.addLayout(main_content_layout)

        self.button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        checked_cast(pyqtBoundSignal, self.button_box.clicked).connect(self.accept)  # pyright: ignore[reportUnknownMemberType]
        window_layout.addWidget(self.button_box)

        self.setLayout(window_layout)

def show_japanese_options() -> None:
    from aqt import mw
    JapaneseOptionsDialog(checked_cast(QWidget, mw)).exec()
