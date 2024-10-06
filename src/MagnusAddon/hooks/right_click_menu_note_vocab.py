from PyQt6.QtWidgets import QMenu

from ankiutils import app, query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_single_vocab_lookup_action, add_text_vocab_lookup, add_ui_action, add_vocab_dependencies_lookup
from note.note_constants import NoteFields, NoteTypes
from note.vocabnote import VocabNote
from sysutils import ex_str
from sysutils.typed import checked_cast

def setup_note_menu(vocab: VocabNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Open"))
    note_hide_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Hide/Remove"))
    note_restore_menu = checked_cast(QMenu, note_menu.addMenu("&Restore"))

    add_lookup_action(note_lookup_menu, "&Kanji", f"note:{NoteTypes.Kanji} ( {' OR '.join([f'{NoteFields.Kanji.question}:{char}' for char in vocab.get_question()])} )")
    if vocab.get_related_ergative_twin():
        add_single_vocab_lookup_action(note_lookup_menu, "Ergative &twin", vocab.get_related_ergative_twin())

    add_lookup_action(note_lookup_menu, "S&entences I'm Studying", query_builder.notes_lookup(vocab.get_sentences_studying()))
    add_lookup_action(note_lookup_menu, "&Sentences", query_builder.notes_lookup(vocab.get_sentences()))
    add_lookup_action(note_lookup_menu, "Sentences with &primary form", query_builder.notes_lookup(vocab.get_sentences_with_primary_form()))

    add_text_vocab_lookup(note_lookup_menu, "&Compounds", vocab.get_question())
    add_vocab_dependencies_lookup(note_lookup_menu, "&Dependencies", vocab)

    for reading in vocab.get_readings():
        add_lookup_action(note_lookup_menu, f"&Homonyms: {reading}", query_builder.notes_lookup(app.col().vocab.with_reading(reading)))

    if not vocab.get_mnemonics_override():
        add_ui_action(note_hide_menu, "&Mnemonic", lambda: vocab.override_meaning_mnemonic())
    if vocab.get_mnemonics_override() == "-":
        add_ui_action(note_restore_menu, "&Mnemonic", lambda: vocab.restore_meaning_mnemonic())
    if not vocab.get_user_answer():
        add_ui_action(note_menu, "Accept &meaning", lambda: vocab.set_user_answer(format_vocab_meaning(vocab.get_answer())))

    for string_menu, menu_string in string_menus:
        vocab_add_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("&Add"))
        add_ui_action(vocab_add_menu, "S&imilar meaning", lambda _menu_string=menu_string: vocab.add_related_similar_meaning(_menu_string)) # type: ignore
        add_ui_action(vocab_add_menu, "&Confused with", lambda _menu_string=menu_string: vocab.add_related_confused_with(_menu_string))  # type: ignore

    for string_menu, menu_string in string_menus:
        note_set_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("&Set"))
        add_ui_action(note_set_menu, "&Meaning", lambda _menu_string=menu_string: vocab.set_user_answer(_menu_string)) # type: ignore
        add_ui_action(note_set_menu, "&Derived from", lambda _menu_string=menu_string: vocab.set_related_derived_from(_menu_string)) # type: ignore
        add_ui_action(note_set_menu, "&Ergative twin", lambda _menu_string=menu_string: vocab.set_related_ergative_twin(_menu_string)) # type: ignore

    for string_menu, menu_string in string_menus:
        sentences = app.col().sentences.with_question(menu_string)
        if sentences:
            sentence = sentences[0]

            sentence_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("S&entence"))

            if vocab.get_question() in sentence.get_user_highlighted_vocab():
                add_ui_action(sentence_menu, "R&emove highlight", lambda _sentence=sentence: _sentence.remove_extra_vocab(vocab.get_question()))  # type: ignore
            else:
                add_ui_action(sentence_menu, "H&ighlight", lambda _sentence=sentence: _sentence.position_extra_vocab(vocab.get_question()))  # type: ignore

            add_ui_action(sentence_menu, "Excl&ude this vocab", lambda _sentence=sentence: _sentence.exclude_vocab(vocab.get_question()))  # type: ignore

    add_ui_action(note_menu, "&Generate answer", lambda: vocab.generate_and_set_answer())
    if vocab.can_generate_sentences_from_context_sentences(require_audio=False):
        add_ui_action(note_menu, "&Generate sentences", lambda: vocab.generate_sentences_from_context_sentences(require_audio=False))

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())
