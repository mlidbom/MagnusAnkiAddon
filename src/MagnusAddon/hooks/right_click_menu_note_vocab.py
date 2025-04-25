from typing import Callable

from PyQt6.QtWidgets import QMenu

from ankiutils import app, query_builder, search_executor
from hooks.right_click_menu_utils import add_lookup_action, add_single_vocab_lookup_action, add_text_vocab_lookup, add_ui_action, add_vocab_dependencies_lookup
from note.note_constants import NoteFields, NoteTypes
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_str
from sysutils.typed import non_optional
from hooks import shortcutfinger

def setup_note_menu(vocab: VocabNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu = non_optional(note_menu.addMenu(shortcutfinger.home1("Open")))
    note_hide_menu: QMenu = non_optional(note_menu.addMenu(shortcutfinger.home2("Hide/Remove")))
    note_restore_menu = non_optional(note_menu.addMenu(shortcutfinger.home3("Restore")))
    note_create_menu = non_optional(note_menu.addMenu(shortcutfinger.up4("Create")))

    add_lookup_action(note_lookup_menu, shortcutfinger.home1("Kanji"), f"note:{NoteTypes.Kanji} ( {' OR '.join([f'{NoteFields.Kanji.question}:{char}' for char in vocab.get_question()])} )")
    if vocab.get_related_ergative_twin():
        add_single_vocab_lookup_action(note_lookup_menu, shortcutfinger.home2("Ergative twin"), vocab.get_related_ergative_twin())

    add_lookup_action(note_lookup_menu, shortcutfinger.home3("Sentences I'm Studying"), query_builder.notes_lookup(vocab.get_sentences_studying()))
    add_lookup_action(note_lookup_menu, shortcutfinger.home4("Sentences"), query_builder.notes_lookup(vocab.get_sentences()))
    add_lookup_action(note_lookup_menu, shortcutfinger.up1("Sentences with primary form"), query_builder.notes_lookup(vocab.get_sentences_with_primary_form()))
    add_lookup_action(note_lookup_menu, shortcutfinger.up2("Sentences with this word highlighted"), query_builder.notes_lookup(vocab.get_user_highlighted_sentences()))

    add_text_vocab_lookup(note_lookup_menu, shortcutfinger.up3("Compounds"), vocab.get_question())
    add_vocab_dependencies_lookup(note_lookup_menu, shortcutfinger.up3("Dependencies"), vocab)

    for reading in vocab.get_readings():
        add_lookup_action(note_lookup_menu, shortcutfinger.up4(f"Homonyms: {reading}"), query_builder.notes_lookup(app.col().vocab.with_reading(reading)))

    if not vocab.get_mnemonics_override():
        add_ui_action(note_hide_menu, shortcutfinger.home1("Mnemonic"), lambda: vocab.override_meaning_mnemonic())
    if vocab.get_mnemonics_override() == "-":
        add_ui_action(note_restore_menu, shortcutfinger.home1("Mnemonic"), lambda: vocab.restore_meaning_mnemonic())
    if not vocab.get_user_answer():
        add_ui_action(note_menu, shortcutfinger.up1("Accept meaning"), lambda: vocab.set_user_answer(format_vocab_meaning(vocab.get_answer())))

    def remove_highlight(_sentences: list[SentenceNote]) -> None:
        for _sentence in _sentences:
            _sentence.remove_extra_vocab(vocab.get_question())

    def exclude(_sentences: list[SentenceNote]) -> None:
        for _sentence in _sentences:
            _sentence.exclude_vocab(vocab.get_question())

    for string_menu, menu_string in string_menus:
        sentences = app.col().sentences.with_question(menu_string)
        if sentences:
            sentence = sentences[0]
            sentence_menu: QMenu = non_optional(string_menu.addMenu(shortcutfinger.home1("Sentence")))

            if vocab.get_question() not in sentence.get_user_highlighted_vocab():
                add_ui_action(sentence_menu, shortcutfinger.home1("Add Highlight"), lambda _sentence=sentence: _sentence.position_extra_vocab(vocab.get_question()))  # type: ignore
            else:
                # noinspection PyDefaultArgument
                add_ui_action(sentence_menu, shortcutfinger.home2("Remove highlight"), lambda _sentences=sentences: remove_highlight(_sentences))  # type: ignore

            # noinspection PyDefaultArgument
            add_ui_action(sentence_menu, shortcutfinger.home3("Exclude this vocab"), lambda _sentences=sentences: exclude(_sentences))  # type: ignore

    for string_menu, menu_string in string_menus:
        vocab_add_menu: QMenu = non_optional(string_menu.addMenu(shortcutfinger.home2("Add")))
        add_ui_action(vocab_add_menu, shortcutfinger.home1("Similar meaning"), lambda _menu_string=menu_string: vocab.add_related_similar_meaning(_menu_string)) # type: ignore
        add_ui_action(vocab_add_menu, shortcutfinger.home2("Confused with"), lambda _menu_string=menu_string: vocab.add_related_confused_with(_menu_string))  # type: ignore

    for string_menu, menu_string in string_menus:
        note_set_menu: QMenu = non_optional(string_menu.addMenu(shortcutfinger.home3("Set")))
        add_ui_action(note_set_menu, shortcutfinger.home1("Derived from"), lambda _menu_string=menu_string: vocab.set_related_derived_from(_menu_string)) # type: ignore
        add_ui_action(note_set_menu, shortcutfinger.home2("Ergative twin"), lambda _menu_string=menu_string: vocab.set_related_ergative_twin(_menu_string)) # type: ignore

    add_ui_action(note_menu, shortcutfinger.up2("Generate answer"), lambda: vocab.generate_and_set_answer())
    if vocab.can_generate_sentences_from_context_sentences(require_audio=False):
        add_ui_action(note_menu, shortcutfinger.up3("Generate sentences"), lambda: vocab.generate_sentences_from_context_sentences(require_audio=False))

    create_note_action(note_create_menu, "な-adjective", lambda: vocab.create_na_adjective(), trigger_tts=True)
    create_note_action(note_create_menu, "に-adverb", lambda: vocab.create_ni_adverb(), trigger_tts=True)
    create_note_action(note_create_menu, "to-adverb", lambda: vocab.create_to_adverb(), trigger_tts=True)
    create_note_action(note_create_menu, "する-verb", lambda: vocab.create_suru_verb(), trigger_tts=True)

    clone_to_form_menu = non_optional(note_create_menu.addMenu("Create form"))
    forms_with_no_vocab = [form for form in vocab.get_forms() if not any(app.col().vocab.with_question(form))]
    for form in forms_with_no_vocab:
        create_note_action(clone_to_form_menu, form, lambda _form=form: vocab.clone_to_form(_form)) # type: ignore

def create_note_action(menu: QMenu, name: str, callback: Callable[[], VocabNote], trigger_tts:bool = False) -> None:
    def run_ui_action() -> None:
        new_note = callback()
        search_executor.do_lookup_and_show_previewer(query_builder.notes_lookup([new_note]))
        if trigger_tts:
            app.ui_utils().trigger_hypertts_button()

    menu.addAction(name, lambda: run_ui_action())

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())
