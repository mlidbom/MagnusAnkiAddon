from __future__ import annotations

from typing import TYPE_CHECKING

import pyperclip  # type: ignore
from ankiutils import app, query_builder
from hooks import shortcutfinger
from hooks.right_click_menu_note_vocab_create_note_menu import build_create_note_menu
from hooks.right_click_menu_utils import add_lookup_action, add_single_vocab_lookup_action, add_ui_action, add_vocab_dependencies_lookup
from note.note_constants import NoteFields, NoteTypes
from note.vocabulary import vocabnote_context_sentences
from sysutils import ex_sequence, ex_str
from sysutils.ex_str import newline
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from PyQt6.QtWidgets import QMenu

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

            add_lookup_action(vocab_lookup_menu, shortcutfinger.home1("Forms"), query_builder.notes_lookup(ex_sequence.flatten([app.col().vocab.with_question(form) for form in vocab.forms.unexcluded_set()])))
            add_lookup_action(vocab_lookup_menu, shortcutfinger.home2("Compound parts"), query_builder.vocabs_lookup_strings(vocab.compound_parts.get()))
            add_lookup_action(vocab_lookup_menu, shortcutfinger.home3("In compounds"), query_builder.notes_lookup(vocab.related_notes.in_compounds()))
            build_readings_menu(non_optional(vocab_lookup_menu.addMenu(shortcutfinger.home4("Homonyms"))))
            add_vocab_dependencies_lookup(vocab_lookup_menu, shortcutfinger.up1("Dependencies"), vocab)

        build_vocab_lookup_menu(non_optional(note_lookup_menu.addMenu(shortcutfinger.home1("Vocab"))))
        build_sentences_lookup_menu(non_optional(note_lookup_menu.addMenu(shortcutfinger.home2("Sentences"))))

        add_lookup_action(note_lookup_menu, shortcutfinger.home3("Kanji"), f"note:{NoteTypes.Kanji} ( {' OR '.join([f'{NoteFields.Kanji.question}:{char}' for char in vocab.get_question()])} )")
        if vocab.related_notes.ergative_twin():
            add_single_vocab_lookup_action(note_lookup_menu, shortcutfinger.home4("Ergative twin"), vocab.related_notes.ergative_twin())

    def build_note_menu() -> None:
        if not vocab.user_answer.get():
            add_ui_action(note_menu, shortcutfinger.up1("Accept meaning"), lambda: vocab.user_answer.set(format_vocab_meaning(vocab.get_answer())))

        add_ui_action(note_menu, shortcutfinger.up2("Generate answer"), lambda: vocab.generate_and_set_answer())
        if vocabnote_context_sentences.can_generate_sentences_from_context_sentences(vocab, False):
            add_ui_action(note_menu, shortcutfinger.up3("Generate sentences"), lambda: vocabnote_context_sentences.generate_sentences_from_context_sentences(vocab, False))

        from batches import local_note_updater

        add_ui_action(note_menu, shortcutfinger.up4("Reparse matching sentences"), lambda: local_note_updater.reparse_sentences_for_vocab(vocab))
        add_ui_action(note_menu, shortcutfinger.up5("Repopulate TOS"), lambda: vocab.parts_of_speech.set_automatically_from_dictionary())

        add_ui_action(note_menu, shortcutfinger.down1("Autogenerate compounds"), lambda: vocab.compound_parts.auto_generate())

    build_lookup_menu(non_optional(note_menu.addMenu(shortcutfinger.home1("Open"))))
    build_create_note_menu(non_optional(note_menu.addMenu(shortcutfinger.home2("Create"))), vocab, selection, clipboard)
    build_copy_menu(non_optional(note_menu.addMenu(shortcutfinger.home3("Copy"))))
    build_note_menu()

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.replace(" SOURCE", "").replace(", ", "/").replace(" ", "-").lower())
