from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from ankiutils import app
from PyQt6.QtCore import pyqtBoundSignal
from sysutils.typed import checked_cast, non_optional
from ui.menus.menu_utils import shortcutfinger

if TYPE_CHECKING:
    from note.notefields.require_forbid_flag_field import RequireForbidFlagField
    from note.notefields.tag_flag_field import TagFlagField
    from note.vocabulary.vocabnote import VocabNote
    from PyQt6.QtWidgets import QMenu

def build_matching_settings_menu(toggle_flags_menu: QMenu, vocab: VocabNote) -> None:
    def add_tag_field_check_box(menu: QMenu, title: str, field: TagFlagField) -> None:
        add_checkbox(menu, title, field.is_set, field.set_to)

    def add_checkbox(menu: QMenu, title: str, getter: Callable[[], bool], setter: Callable[[bool], None], reparse_sentences: bool = True) -> None:
        def set_value(value: bool) -> None:
            setter(value)
            if reparse_sentences:
                from batches import local_note_updater
                local_note_updater.reparse_sentences_for_vocab(vocab)
            app.get_ui_utils().refresh()

        action = non_optional(menu.addAction(title))
        action.setCheckable(True)
        action.setChecked(getter())
        checked_cast(pyqtBoundSignal, action.triggered).connect(set_value)

    def build_requires_forbids_menu(requires_forbids_menu: QMenu) -> None:
        def add_require_forbid_menu(menu: QMenu, title: str, field: RequireForbidFlagField, reparse_sentences: bool = True) -> None:
            toggle_menu = non_optional(menu.addMenu(title))
            add_checkbox(toggle_menu, shortcutfinger.home1("Required"), lambda: field.is_configured_required, field.set_required, reparse_sentences)
            add_checkbox(toggle_menu, shortcutfinger.home2("Forbidden"), lambda: field.is_configured_forbidden, field.set_forbidden, reparse_sentences)

        def build_misc_menu(misc_menu: QMenu) -> None:
            add_require_forbid_menu(misc_menu, shortcutfinger.home1("exact match"), vocab.matching_configuration.requires_forbids.requires_exact_match)
            add_require_forbid_menu(misc_menu, shortcutfinger.home2("single token"), vocab.matching_configuration.requires_forbids.single_token)
            add_require_forbid_menu(misc_menu, shortcutfinger.home3("Sentence end"), vocab.matching_configuration.requires_forbids.sentence_end)

        def build_stem_menu(stem_menu: QMenu) -> None:
            add_require_forbid_menu(stem_menu, shortcutfinger.home1("e stem"), vocab.matching_configuration.requires_forbids.e_stem)
            add_require_forbid_menu(stem_menu, shortcutfinger.home2("a stem"), vocab.matching_configuration.requires_forbids.a_stem)
            add_require_forbid_menu(stem_menu, shortcutfinger.home3("past tense stem"), vocab.matching_configuration.requires_forbids.past_tense_stem)
            add_require_forbid_menu(stem_menu, shortcutfinger.home4("て-form stem"), vocab.matching_configuration.requires_forbids.t_form_stem)

        add_require_forbid_menu(requires_forbids_menu, shortcutfinger.home1("Display: yield to overlapping following compound"), vocab.matching_configuration.requires_forbids.yield_last_token, reparse_sentences=False)
        build_misc_menu(non_optional(requires_forbids_menu.addMenu(shortcutfinger.home2("Misc matching rules"))))
        build_stem_menu(non_optional(requires_forbids_menu.addMenu(shortcutfinger.home3("Stem matching rules"))))

    def build_is_menu(is_menu: QMenu) -> None:
        add_tag_field_check_box(is_menu, shortcutfinger.home1("Poison word"), vocab.matching_configuration.bool_flags.is_poison_word)
        add_tag_field_check_box(is_menu, shortcutfinger.home2("Inflecting word"), vocab.matching_configuration.bool_flags.is_inflecting_word)

    def build_misc_flags_menu(misc_menu: QMenu) -> None:
        add_tag_field_check_box(misc_menu, shortcutfinger.home1("Question overrides form: Show the question in results even if the match was another form"), vocab.matching_configuration.bool_flags.question_overrides_form.tag_field)
        add_tag_field_check_box(misc_menu, shortcutfinger.home3("Match with preceding vowel"), vocab.matching_configuration.bool_flags.match_with_preceding_vowel)

    build_requires_forbids_menu(non_optional(toggle_flags_menu.addMenu(shortcutfinger.home1("Requireds/Forbids"))))
    build_is_menu(non_optional(toggle_flags_menu.addMenu(shortcutfinger.home2("Is"))))
    build_misc_flags_menu(non_optional(toggle_flags_menu.addMenu(shortcutfinger.home3("Misc"))))
