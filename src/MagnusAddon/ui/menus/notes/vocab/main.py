from __future__ import annotations

from typing import TYPE_CHECKING

import pyperclip
from ankiutils import app, query_builder
from aqt import qconnect
from note.note_constants import NoteFields, NoteTypes
from note.vocabulary import vocabnote_context_sentences
from sysutils import ex_sequence, ex_str
from sysutils.ex_str import newline
from sysutils.typed import non_optional
from ui.menus.menu_utils import shortcutfinger
from ui.menus.menu_utils.ex_qmenu import add_lookup_action, add_single_vocab_lookup_action, add_ui_action, add_vocab_dependencies_lookup
from ui.menus.notes.vocab.create_note_menu import build_create_note_menu

if TYPE_CHECKING:
    from note.notefields.tag_flag_field import TagFlagField
    from note.vocabulary.vocabnote import VocabNote
    from PyQt6.QtWidgets import QMenu

def add_toggle_checkbox(menu: QMenu, title: str, field: TagFlagField) -> None:
    def set_value(value: bool) -> None:
        field.set_to(value)
        app.get_ui_utils().refresh()

    action = menu.addAction(title)
    action.setCheckable(True)
    action.setChecked(field.is_set)
    qconnect(action.triggered, set_value)

def setup_note_menu(note_menu: QMenu, vocab: VocabNote, selection: str, clipboard: str) -> None:
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
                    add_lookup_action(readings_vocab_lookup_menu, shortcutfinger.numpad_no_numbers(index, f"Homonyms: {reading}"), query_builder.notes_lookup(app.col().vocab.with_reading(reading)))

            add_lookup_action(vocab_lookup_menu, shortcutfinger.home1("Forms"), query_builder.notes_lookup(ex_sequence.flatten([app.col().vocab.with_question(form) for form in vocab.forms.all_set()])))
            add_lookup_action(vocab_lookup_menu, shortcutfinger.home2("Compound parts"), query_builder.vocabs_lookup_strings(vocab.compound_parts.get()))
            add_lookup_action(vocab_lookup_menu, shortcutfinger.home3("In compounds"), query_builder.notes_lookup(vocab.related_notes.in_compounds()))
            add_lookup_action(vocab_lookup_menu, shortcutfinger.home4("Synonyms"), query_builder.notes_lookup(vocab.related_notes.synonyms.notes()))
            build_readings_menu(non_optional(vocab_lookup_menu.addMenu(shortcutfinger.up1("Homonyms"))))
            add_vocab_dependencies_lookup(vocab_lookup_menu, shortcutfinger.up2("Dependencies"), vocab)

        build_vocab_lookup_menu(non_optional(note_lookup_menu.addMenu(shortcutfinger.home1("Vocab"))))
        build_sentences_lookup_menu(non_optional(note_lookup_menu.addMenu(shortcutfinger.home2("Sentences"))))

        add_lookup_action(note_lookup_menu, shortcutfinger.home3("Kanji"), f"note:{NoteTypes.Kanji} ( {' OR '.join([f'{NoteFields.Kanji.question}:{char}' for char in vocab.get_question()])} )")
        if vocab.related_notes.ergative_twin.get():
            related_vocab = vocab.related_notes
            add_single_vocab_lookup_action(note_lookup_menu, shortcutfinger.home4("Ergative twin"), related_vocab.ergative_twin.get())

    def build_note_menu() -> None:
        if not vocab.user.answer.get():
            add_ui_action(note_menu, shortcutfinger.up1("Accept meaning"), lambda: vocab.user.answer.set(format_vocab_meaning(vocab.get_answer())))

        add_ui_action(note_menu, shortcutfinger.up2("Generate answer"), lambda: vocab.generate_and_set_answer())
        if vocabnote_context_sentences.can_generate_sentences_from_context_sentences(vocab, False):
            add_ui_action(note_menu, shortcutfinger.up3("Generate sentences"), lambda: vocabnote_context_sentences.generate_sentences_from_context_sentences(vocab, False))

        from batches import local_note_updater

        add_ui_action(note_menu, shortcutfinger.up4("Reparse matching sentences"), lambda: local_note_updater.reparse_sentences_for_vocab(vocab))
        add_ui_action(note_menu, shortcutfinger.up5("Repopulate TOS"), lambda: vocab.parts_of_speech.set_automatically_from_dictionary())

        add_ui_action(note_menu, shortcutfinger.down1("Autogenerate compounds"), lambda: vocab.compound_parts.auto_generate())

    def build_toggle_flags_menu(toggle_flags_menu: QMenu) -> None:
        add_toggle_checkbox(toggle_flags_menu, shortcutfinger.home1("Requires exact match"), vocab.matching_rules.requires_exact_match)
        add_toggle_checkbox(toggle_flags_menu, shortcutfinger.home2("Requires e stem"), vocab.matching_rules.requires_e_stem)
        add_toggle_checkbox(toggle_flags_menu, shortcutfinger.home3("Requires a stem"), vocab.matching_rules.requires_a_stem)
        add_toggle_checkbox(toggle_flags_menu, shortcutfinger.home4("Match with preceding vowel"), vocab.matching_rules.match_with_preceding_vowel)
        add_toggle_checkbox(toggle_flags_menu, shortcutfinger.home5("Question overrides form"), vocab.matching_rules.question_overrides_form)

    def build_remove_menu(remove_menu: QMenu) -> None:
        add_ui_action(remove_menu, shortcutfinger.home1("User explanation"), lambda: vocab.user.explanation.empty()).setEnabled(vocab.user.explanation.has_value())
        add_ui_action(remove_menu, shortcutfinger.home2("User explanation long"), lambda: vocab.user.explanation_long.empty()).setEnabled(vocab.user.explanation_long.has_value())
        add_ui_action(remove_menu, shortcutfinger.home3("User mnemonic"), lambda: vocab.user.mnemonic.empty()).setEnabled(vocab.user.mnemonic.has_value())
        add_ui_action(remove_menu, shortcutfinger.home4("User answer"), lambda: vocab.user.answer.empty(), True).setEnabled(vocab.user.answer.has_value())

    build_lookup_menu(non_optional(note_menu.addMenu(shortcutfinger.home1("Open"))))
    build_create_note_menu(non_optional(note_menu.addMenu(shortcutfinger.home2("Create"))), vocab, selection, clipboard)
    build_copy_menu(non_optional(note_menu.addMenu(shortcutfinger.home3("Copy"))))
    build_toggle_flags_menu(non_optional(note_menu.addMenu(shortcutfinger.home4("Toggle flags"))))
    build_remove_menu(non_optional(note_menu.addMenu(shortcutfinger.up1("Remove"))))
    build_note_menu()

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.replace(" SOURCE", "").replace(", ", "/").replace(" ", "-").lower())
