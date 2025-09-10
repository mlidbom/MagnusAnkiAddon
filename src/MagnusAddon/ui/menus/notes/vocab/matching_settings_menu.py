from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import pyperclip
from ankiutils import app, query_builder
from aqt import qconnect
from note.note_constants import NoteFields, NoteTypes
from sysutils import ex_sequence, ex_str
from sysutils.ex_str import newline
from sysutils.typed import non_optional
from ui.menus.menu_utils import shortcutfinger
from ui.menus.menu_utils.ex_qmenu import add_lookup_action, add_single_vocab_lookup_action, add_ui_action, add_vocab_dependencies_lookup
from ui.menus.notes.vocab.create_note_menu import build_create_note_menu

if TYPE_CHECKING:
    from note.notefields.require_forbid_flag_field import RequireForbidFlagField
    from note.notefields.tag_flag_field import TagFlagField
    from note.vocabulary.vocabnote import VocabNote
    from PyQt6.QtWidgets import QMenu

def setup_matching_settings_menu(note_menu: QMenu, vocab: VocabNote, selection: str, clipboard: str) -> None:
    def add_tag_field_check_box(menu: QMenu, title: str, field: TagFlagField) -> None:
        add_checkbox(menu, title, field.is_set, field.set_to)

    def add_checkbox(menu: QMenu, title: str, getter: Callable[[], bool], setter: Callable[[bool], None]) -> None:
        def set_value(value: bool) -> None:
            setter(value)
            from batches import local_note_updater
            local_note_updater.reparse_sentences_for_vocab(vocab)
            app.get_ui_utils().refresh()

        action = non_optional(menu.addAction(title))
        action.setCheckable(True)
        action.setChecked(getter())
        qconnect(action.triggered, set_value)

    def build_toggle_flags_menu(toggle_flags_menu: QMenu) -> None:
        def build_requires_forbids_menu(requires_forbids_menu: QMenu) -> None:
            def add_require_forbid_menu(menu: QMenu, title: str, field: RequireForbidFlagField) -> None:
                toggle_menu = non_optional(menu.addMenu(title))
                add_checkbox(toggle_menu, shortcutfinger.home1("Required"), lambda: field.is_configured_required, field.set_required)
                add_checkbox(toggle_menu, shortcutfinger.home2("Forbidden"), lambda: field.is_configured_forbidden, field.set_forbidden)

            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.home2("single token"), vocab.matching_rules.single_token)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.home3("yield to overlapping compound"), vocab.matching_rules.yield_last_token)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.home4("e stem"), vocab.matching_rules.e_stem)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.home5("a stem"), vocab.matching_rules.a_stem)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.up1("paste tense stem"), vocab.matching_rules.past_tense_stem)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.up2("て-form tense stem"), vocab.matching_rules.t_form_stem)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.up3("Sentence end"), vocab.matching_rules.sentence_end)

        def build_is_menu(is_menu: QMenu) -> None:
            add_tag_field_check_box(is_menu, shortcutfinger.home1("Poison word"), vocab.matching_rules.is_poison_word)
            add_tag_field_check_box(is_menu, shortcutfinger.home2("Inflecting word"), vocab.matching_rules.is_inflecting_word)

        def build_misc_flags_menu(misc_menu: QMenu) -> None:
            add_tag_field_check_box(misc_menu, shortcutfinger.home1("Question overrides form: Show the question in results even if the match was another form"), vocab.matching_rules.question_overrides_form.tag_field)
            add_tag_field_check_box(misc_menu, shortcutfinger.home3("Match with preceding vowel"), vocab.matching_rules.match_with_preceding_vowel)

        build_requires_forbids_menu(non_optional(toggle_flags_menu.addMenu(shortcutfinger.home1("Requireds/Forbids"))))
        build_is_menu(non_optional(toggle_flags_menu.addMenu(shortcutfinger.home1("Is"))))
        build_misc_flags_menu(non_optional(toggle_flags_menu.addMenu(shortcutfinger.home3("Misc"))))
        add_tag_field_check_box(toggle_flags_menu, shortcutfinger.home4("Requires exact match"), vocab.matching_rules.requires_exact_match)

    build_create_note_menu(non_optional(note_menu.addMenu(shortcutfinger.home2("Create"))), vocab, selection, clipboard)
    build_toggle_flags_menu(non_optional(note_menu.addMenu(shortcutfinger.home5("Toggle flags"))))