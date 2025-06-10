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

def setup_note_menu(note_menu: QMenu, vocab: VocabNote, selection: str, clipboard: str) -> None:
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

    def build_copy_menu(note_copy_menu: QMenu) -> None:
        note_copy_menu.addAction(shortcutfinger.home1("Question"), lambda: pyperclip.copy(vocab.get_question()))
        note_copy_menu.addAction(shortcutfinger.home2("Answer"), lambda: pyperclip.copy(vocab.get_answer()))
        note_copy_menu.addAction(shortcutfinger.home3("Definition (question:answer)"), lambda: pyperclip.copy(f"""{vocab.get_question()}: {vocab.get_answer()}"""))
        note_copy_menu.addAction(shortcutfinger.home4("Sentences: max 30"), lambda: pyperclip.copy(newline.join([sent.get_question() for sent in vocab.sentences.all()[0:30]])))

    def build_lookup_menu(note_lookup_menu: QMenu) -> None:
        def build_sentences_lookup_menu(sentences_lookup_menu: QMenu) -> None:
            add_lookup_action(sentences_lookup_menu, shortcutfinger.home1("Sentences I'm Studying"), query_builder.notes_lookup(vocab.sentences.studying()))
            add_lookup_action(sentences_lookup_menu, shortcutfinger.home2("Sentences"), query_builder.notes_lookup(vocab.sentences.all()))
            add_lookup_action(sentences_lookup_menu, shortcutfinger.home3("Sentences with primary form"), query_builder.notes_lookup(vocab.sentences.with_primary_form()))
            add_lookup_action(sentences_lookup_menu, shortcutfinger.home4("Sentences with this word highlighted"), query_builder.notes_lookup(vocab.sentences.user_highlighted()))

        def build_vocab_lookup_menu(vocab_lookup_menu: QMenu) -> None:
            def build_readings_menu(readings_vocab_lookup_menu: QMenu) -> None:
                for index, reading in enumerate(vocab.readings.get()):
                    add_lookup_action(readings_vocab_lookup_menu, shortcutfinger.finger_by_priority_order(index, f"Homonyms: {reading}"), query_builder.notes_lookup(app.col().vocab.with_reading(reading)))

            add_lookup_action(vocab_lookup_menu, shortcutfinger.home1("Forms"), query_builder.notes_lookup(ex_sequence.flatten([app.col().vocab.with_question(form) for form in vocab.forms.all_set()])))
            add_lookup_action(vocab_lookup_menu, shortcutfinger.home2("Compound parts"), query_builder.vocabs_lookup_strings(vocab.compound_parts.all()))
            add_lookup_action(vocab_lookup_menu, shortcutfinger.home3("In compounds"), query_builder.notes_lookup(vocab.related_notes.in_compounds()))
            add_lookup_action(vocab_lookup_menu, shortcutfinger.home4("Synonyms"), query_builder.notes_lookup(vocab.related_notes.synonyms.notes()))
            add_lookup_action(vocab_lookup_menu, shortcutfinger.home5("See also"), query_builder.notes_lookup(vocab.related_notes.see_also.notes()))
            build_readings_menu(non_optional(vocab_lookup_menu.addMenu(shortcutfinger.up1("Homonyms"))))
            add_vocab_dependencies_lookup(vocab_lookup_menu, shortcutfinger.up2("Dependencies"), vocab)

        build_vocab_lookup_menu(non_optional(note_lookup_menu.addMenu(shortcutfinger.home1("Vocab"))))
        build_sentences_lookup_menu(non_optional(note_lookup_menu.addMenu(shortcutfinger.home2("Sentences"))))

        add_lookup_action(note_lookup_menu, shortcutfinger.home3("Kanji"), f"note:{NoteTypes.Kanji} ( {' OR '.join([f'{NoteFields.Kanji.question}:{char}' for char in vocab.get_question()])} )")
        if vocab.related_notes.ergative_twin.get():
            related_vocab = vocab.related_notes
            add_single_vocab_lookup_action(note_lookup_menu, shortcutfinger.home4("Ergative twin"), related_vocab.ergative_twin.get())

    def build_misc_menu(misc_menu: QMenu) -> None:
        add_ui_action(misc_menu, shortcutfinger.home1("Accept meaning"), lambda: vocab.user.answer.set(format_vocab_meaning(vocab.get_answer())), not vocab.user.answer.get())
        add_ui_action(misc_menu, shortcutfinger.home2("Generate answer"), lambda: vocab.generate_and_set_answer())

        from batches import local_note_updater
        add_ui_action(misc_menu, shortcutfinger.home3("Reparse potentially matching sentences: (Only reparse all sentences is sure to catch everything)"), lambda: local_note_updater.reparse_sentences_for_vocab(vocab))
        add_ui_action(misc_menu, shortcutfinger.home4("Repopulate TOS"), lambda: vocab.parts_of_speech.set_automatically_from_dictionary())

        add_ui_action(misc_menu, shortcutfinger.home5("Autogenerate compounds"), lambda: vocab.compound_parts.auto_generate())

    def build_toggle_flags_menu(toggle_flags_menu: QMenu) -> None:
        def build_requires_forbids_menu(requires_forbids_menu: QMenu) -> None:
            def add_require_forbid_menu(menu: QMenu, title: str, field: RequireForbidFlagField) -> None:
                toggle_menu = non_optional(menu.addMenu(title))
                add_checkbox(toggle_menu, shortcutfinger.home1("Required"), lambda: field.is_required, field.set_required)
                add_checkbox(toggle_menu, shortcutfinger.home2("Forbidden"), lambda: field.is_forbidden, field.set_forbidden)

            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.home2("single token"), vocab.matching_rules.single_token)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.home4("e stem"), vocab.matching_rules.e_stem)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.home5("a stem"), vocab.matching_rules.a_stem)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.up1("Sentence end"), vocab.matching_rules.sentence_end)
            add_require_forbid_menu(requires_forbids_menu, shortcutfinger.home3("yield to overlapping compound"), vocab.matching_rules.yield_last_token)

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

    def build_remove_menu(remove_menu: QMenu) -> None:
        add_ui_action(remove_menu, shortcutfinger.home1("User explanation"), lambda: vocab.user.explanation.empty()).setEnabled(vocab.user.explanation.has_value())
        add_ui_action(remove_menu, shortcutfinger.home2("User explanation long"), lambda: vocab.user.explanation_long.empty()).setEnabled(vocab.user.explanation_long.has_value())
        add_ui_action(remove_menu, shortcutfinger.home3("User mnemonic"), lambda: vocab.user.mnemonic.empty()).setEnabled(vocab.user.mnemonic.has_value())
        add_ui_action(remove_menu, shortcutfinger.home4("User answer"), lambda: vocab.user.answer.empty(), True).setEnabled(vocab.user.answer.has_value())

    build_lookup_menu(non_optional(note_menu.addMenu(shortcutfinger.home1("Open"))))
    build_create_note_menu(non_optional(note_menu.addMenu(shortcutfinger.home2("Create"))), vocab, selection, clipboard)
    build_copy_menu(non_optional(note_menu.addMenu(shortcutfinger.home3("Copy"))))
    build_misc_menu(non_optional(note_menu.addMenu(shortcutfinger.home4("Misc"))))
    build_toggle_flags_menu(non_optional(note_menu.addMenu(shortcutfinger.home5("Toggle flags"))))
    build_remove_menu(non_optional(note_menu.addMenu(shortcutfinger.up1("Remove"))))

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.replace(" SOURCE", "").replace(", ", "/").replace(" ", "-").lower())

def build_view_menu(_view_menu: QMenu, _vocab: VocabNote) -> None:
    pass
