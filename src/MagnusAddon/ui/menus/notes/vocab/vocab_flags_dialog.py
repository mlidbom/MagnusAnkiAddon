from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QMessageBox, QScrollArea, QVBoxLayout, QWidget
from sysutils.typed import checked_cast
from ui.menus.notes.vocab.require_forbid_widget import RequireForbidWidget
from ui.menus.notes.vocab.string_set_widget import StringSetWidget

if TYPE_CHECKING:
    from note.notefields.require_forbid_flag_field import RequireForbidFlagField
    from note.notefields.tag_flag_field import TagFlagField
    from note.vocabulary.vocabnote import VocabNote

class VocabFlagsDialog(QDialog):
    def __init__(self, vocab: VocabNote, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.vocab = vocab
        self.changed_reparse_flags: set[str] = set()

        self.setWindowTitle(f"Edit Flags: {vocab.get_question()}")

        main_layout = QVBoxLayout()

        # Create scroll area for content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        
        # Create horizontal layout for left and right sections
        content_layout = QHBoxLayout()

        # Left column
        left_layout = QVBoxLayout()
        self._build_matching_settings_section(left_layout)
        left_layout.addStretch()

        # Right column
        right_layout = QVBoxLayout()
        self._build_metadata_section(right_layout)
        right_layout.addStretch()

        content_layout.addLayout(left_layout)
        content_layout.addLayout(right_layout)

        self.scroll_content.setLayout(content_layout)
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # Add button box
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        checked_cast(pyqtBoundSignal, self.button_box.accepted).connect(self.accept)  # pyright: ignore[reportUnknownMemberType]
        checked_cast(pyqtBoundSignal, self.button_box.rejected).connect(self.reject)  # pyright: ignore[reportUnknownMemberType]
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)
        
        # Auto-size the dialog to fit content, but constrain to screen size
        self._auto_resize_to_content()

    def _auto_resize_to_content(self) -> None:
        """Auto-resize dialog to fit content while respecting screen boundaries."""
        # Get the screen geometry
        screen = self.screen()
        if screen is None:
            # Fallback if we can't get screen info
            self.resize(1200, 800)
            return
        
        screen_geometry = screen.availableGeometry()
        
        # Force layout updates to get accurate sizes
        self.scroll_content.adjustSize()
        content_size = self.scroll_content.sizeHint()
        
        # Calculate total needed height: content + button box + margins
        button_box_height = self.button_box.sizeHint().height()
        dialog_margins = self.layout().contentsMargins()
        vertical_margins = dialog_margins.top() + dialog_margins.bottom()
        
        # Add some padding for scrollbar appearance threshold
        needed_height = content_size.height() + button_box_height + vertical_margins + 20
        needed_width = max(content_size.width() + 40, 1200)  # Content width + some margin, min 1200
        
        # Constrain to screen size (90%)
        max_width = int(screen_geometry.width() * 0.9)
        max_height = int(screen_geometry.height() * 0.9)
        
        final_width = min(needed_width, max_width)
        final_height = min(needed_height, max_height)
        
        self.resize(final_width, final_height)

    def _add_checkbox(self, layout: QVBoxLayout, title: str, field: TagFlagField, reparse_trigger: bool = True) -> None:
        checkbox = QCheckBox(title)
        initial_value = field.is_set()
        checkbox.setChecked(initial_value)

        def on_changed(checked: bool) -> None:
            field.set_to(checked)
            if reparse_trigger and checked != initial_value:
                self.changed_reparse_flags.add(title)
            elif title in self.changed_reparse_flags and checked == initial_value:
                self.changed_reparse_flags.remove(title)

        checked_cast(pyqtBoundSignal, checkbox.toggled).connect(on_changed)  # pyright: ignore[reportUnknownMemberType]
        layout.addWidget(checkbox)

    def _on_reparse_flag_changed(self, title: str, should_add: bool) -> None:
        """Callback for widgets to notify when a reparse-triggering flag changes."""
        if should_add:
            self.changed_reparse_flags.add(title)
        elif title in self.changed_reparse_flags:
            self.changed_reparse_flags.remove(title)

    def _add_require_forbid_field(self, grid: QGridLayout, row: int, title: str, field: RequireForbidFlagField, reparse_trigger: bool = True) -> None:
        label = QLabel(title)
        grid.addWidget(label, row, 0)

        widget = RequireForbidWidget(field, title, self._on_reparse_flag_changed, reparse_trigger)
        grid.addWidget(widget, row, 1)

    def _build_matching_settings_section(self, main_layout: QVBoxLayout) -> None:
        matching_settings_group = QGroupBox("Parsing")
        matching_settings_group.setSizePolicy(matching_settings_group.sizePolicy().horizontalPolicy(), matching_settings_group.sizePolicy().verticalPolicy())
        layout = QVBoxLayout()

        # Requires/Forbids Display section
        display_group = QGroupBox("Display")
        display_grid = QGridLayout()
        display_grid.setColumnStretch(0, 0)
        display_grid.setColumnStretch(1, 0)
        self._add_require_forbid_field(display_grid, 0, "Yield to overlapping following compound",
                                       self.vocab.matching_configuration.requires_forbids.yield_last_token, False)
        display_group.setLayout(display_grid)
        layout.addWidget(display_group)

        # Misc matching rules section
        misc_matching_group = QGroupBox("Misc matching rules")
        misc_matching_grid = QGridLayout()
        misc_matching_grid.setColumnStretch(0, 0)
        misc_matching_grid.setColumnStretch(1, 0)
        self._add_require_forbid_field(misc_matching_grid, 0, "Exact match", self.vocab.matching_configuration.requires_forbids.exact_match)
        self._add_require_forbid_field(misc_matching_grid, 1, "Sentence end", self.vocab.matching_configuration.requires_forbids.sentence_end)
        self._add_require_forbid_field(misc_matching_grid, 2, "Sentence start", self.vocab.matching_configuration.requires_forbids.sentence_start)
        self._add_require_forbid_field(misc_matching_grid, 3, "Single token", self.vocab.matching_configuration.requires_forbids.single_token)
        misc_matching_group.setLayout(misc_matching_grid)
        layout.addWidget(misc_matching_group)

        # Stem matching rules section
        stem_group = QGroupBox("Stem matching rules")
        stem_grid = QGridLayout()
        stem_grid.setColumnStretch(0, 0)
        stem_grid.setColumnStretch(1, 0)
        self._add_require_forbid_field(stem_grid, 0, "A stem", self.vocab.matching_configuration.requires_forbids.a_stem)
        self._add_require_forbid_field(stem_grid, 1, "E stem", self.vocab.matching_configuration.requires_forbids.e_stem)
        self._add_require_forbid_field(stem_grid, 2, "Godan imperative", self.vocab.matching_configuration.requires_forbids.godan_imperative)
        self._add_require_forbid_field(stem_grid, 3, "Godan imperative prefix", self.vocab.matching_configuration.requires_forbids.godan_imperative_prefix)
        self._add_require_forbid_field(stem_grid, 4, "Godan potential", self.vocab.matching_configuration.requires_forbids.godan_potential)
        self._add_require_forbid_field(stem_grid, 5, "Ichidan imperative", self.vocab.matching_configuration.requires_forbids.ichidan_imperative)
        self._add_require_forbid_field(stem_grid, 6, "Masu stem", self.vocab.matching_configuration.requires_forbids.masu_stem)
        self._add_require_forbid_field(stem_grid, 7, "Past tense stem", self.vocab.matching_configuration.requires_forbids.past_tense_stem)
        self._add_require_forbid_field(stem_grid, 8, "Dictionary form stem", self.vocab.matching_configuration.requires_forbids.dictionary_form_stem)
        self._add_require_forbid_field(stem_grid, 9, "Preceding adverb", self.vocab.matching_configuration.requires_forbids.preceding_adverb)
        self._add_require_forbid_field(stem_grid, 10, "て-form stem", self.vocab.matching_configuration.requires_forbids.te_form_stem)
        stem_group.setLayout(stem_grid)
        layout.addWidget(stem_group)

        # Is section
        is_group = QGroupBox("Is")
        is_layout = QVBoxLayout()
        self._add_checkbox(is_layout, "Inflecting word", self.vocab.matching_configuration.bool_flags.is_inflecting_word)
        self._add_checkbox(is_layout, "Poison word", self.vocab.matching_configuration.bool_flags.is_poison_word)
        is_group.setLayout(is_layout)
        layout.addWidget(is_group)

        # Misc section
        misc_group = QGroupBox("Misc")
        misc_layout = QVBoxLayout()
        self._add_checkbox(misc_layout, "Match with preceding vowel",
                           self.vocab.matching_configuration.bool_flags.match_with_preceding_vowel)
        self._add_checkbox(misc_layout, "Question overrides form: Show the question in results even if the match was another form",
                           self.vocab.matching_configuration.bool_flags.question_overrides_form)
        misc_group.setLayout(misc_layout)
        layout.addWidget(misc_group)

        # String Rules section
        self._build_string_rules_section(layout)

        matching_settings_group.setLayout(layout)
        main_layout.addWidget(matching_settings_group)

    def _build_string_rules_section(self, parent_layout: QVBoxLayout) -> None:
        """Build the string rules section with editable string sets."""
        string_rules_group = QGroupBox("String Rules")
        layout = QVBoxLayout()
        
        # Add widgets for each string set in alphabetical order
        layout.addWidget(StringSetWidget(self.vocab.matching_configuration.configurable_rules.prefix_is_not, "Prefix is not"))
        layout.addWidget(StringSetWidget(self.vocab.matching_configuration.configurable_rules.required_prefix, "Required prefix"))
        layout.addWidget(StringSetWidget(self.vocab.matching_configuration.configurable_rules.suffix_is_not, "Suffix is not"))
        layout.addWidget(StringSetWidget(self.vocab.matching_configuration.configurable_rules.surface_is_not, "Surface is not"))
        layout.addWidget(StringSetWidget(self.vocab.matching_configuration.configurable_rules.yield_to_surface, "Yield to surface"))
        
        string_rules_group.setLayout(layout)
        parent_layout.addWidget(string_rules_group)

    def _build_metadata_section(self, main_layout: QVBoxLayout) -> None:
        metadata_group = QGroupBox("Meta Data")
        layout = QVBoxLayout()

        # Misc section
        misc_group = QGroupBox("Misc")
        misc_layout = QVBoxLayout()
        self._add_checkbox(misc_layout, "Compositionally transparent compound",
                           self.vocab.matching_configuration.bool_flags.is_compositionally_transparent_compound, False)
        misc_group.setLayout(misc_layout)
        layout.addWidget(misc_group)

        # Register section
        self._build_register_section_content(layout)

        metadata_group.setLayout(layout)
        main_layout.addWidget(metadata_group)

    def _build_register_section_content(self, parent_layout: QVBoxLayout) -> None:
        register_group = QGroupBox("Register")
        layout = QVBoxLayout()

        self._add_checkbox(layout, "Archaic", self.vocab.register.archaic, False)
        self._add_checkbox(layout, "Childish", self.vocab.register.childish, False)
        self._add_checkbox(layout, "Derogatory", self.vocab.register.derogatory, False)
        self._add_checkbox(layout, "Formal", self.vocab.register.formal, False)
        self._add_checkbox(layout, "Honorific", self.vocab.register.honorific, False)
        self._add_checkbox(layout, "Humble", self.vocab.register.humble, False)
        self._add_checkbox(layout, "Informal", self.vocab.register.informal, False)
        self._add_checkbox(layout, "Literary", self.vocab.register.literary, False)
        self._add_checkbox(layout, "Polite", self.vocab.register.polite, False)
        self._add_checkbox(layout, "Rough, traditionally considered male", self.vocab.register.rough_masculine, False)
        self._add_checkbox(layout, "Slang", self.vocab.register.slang, False)
        self._add_checkbox(layout, "Soft, traditionally considered feminine", self.vocab.register.soft_feminine, False)
        self._add_checkbox(layout, "Vulgar, usually offensive", self.vocab.register.vulgar, False)

        register_group.setLayout(layout)
        parent_layout.addWidget(register_group)

    def accept(self) -> None:
        """Override accept to check if reparsing is needed."""
        if self.changed_reparse_flags:
            reply = QMessageBox.question(
                    self,
                    "Reparse Sentences?",
                    "You changed settings that affect sentence parsing. Would you like to reparse sentences for this vocab now?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes
            )

            if reply == QMessageBox.StandardButton.Yes:
                from batches import local_note_updater
                local_note_updater.reparse_sentences_for_vocab(self.vocab)

        app.get_ui_utils().refresh()

        super().accept()

def show_vocab_flags_dialog(vocab: VocabNote, parent: QWidget | None = None) -> None:
    dialog = VocabFlagsDialog(vocab, parent)
    dialog.exec()
