from PyQt6.QtWidgets import QMenu

from ankiutils import app, query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_single_vocab_lookup_action, add_text_vocab_lookup, add_ui_action, add_vocab_dependencies_lookup
from note.note_constants import NoteFields, NoteTypes
from note.vocabnote import VocabNote
from sysutils import ex_str
from sysutils.typed import checked_cast
from hooks import shortcutfinger

def setup_note_menu(vocab: VocabNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu = checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home1("Open")))
    note_hide_menu: QMenu = checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home2("Hide/Remove")))
    note_restore_menu = checked_cast(QMenu, note_menu.addMenu(shortcutfinger.home3("Restore")))

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
        add_ui_action(note_menu, shortcutfinger.home4("Accept meaning"), lambda: vocab.set_user_answer(format_vocab_meaning(vocab.get_answer())))

    for string_menu, menu_string in string_menus:
        sentences = app.col().sentences.with_question(menu_string)
        if sentences:
            sentence = sentences[0]
            sentence_menu: QMenu = checked_cast(QMenu, string_menu.addMenu(shortcutfinger.home1("Sentence")))

            if vocab.get_question() not in sentence.get_user_highlighted_vocab():
                add_ui_action(sentence_menu, shortcutfinger.home1("Add Highlight"), lambda _sentence=sentence: _sentence.position_extra_vocab(vocab.get_question()))  # type: ignore
            else:
                add_ui_action(sentence_menu, shortcutfinger.home2("Remove highlight"), lambda _sentence=sentence: _sentence.remove_extra_vocab(vocab.get_question()))  # type: ignore


            add_ui_action(sentence_menu, shortcutfinger.home3("Exclude this vocab"), lambda _sentence=sentence: _sentence.exclude_vocab(vocab.get_question()))  # type: ignore

    for string_menu, menu_string in string_menus:
        vocab_add_menu: QMenu = checked_cast(QMenu, string_menu.addMenu(shortcutfinger.home2("Add")))
        add_ui_action(vocab_add_menu, shortcutfinger.home1("Similar meaning"), lambda _menu_string=menu_string: vocab.add_related_similar_meaning(_menu_string)) # type: ignore
        add_ui_action(vocab_add_menu, shortcutfinger.home2("Confused with"), lambda _menu_string=menu_string: vocab.add_related_confused_with(_menu_string))  # type: ignore

    for string_menu, menu_string in string_menus:
        note_set_menu: QMenu = checked_cast(QMenu, string_menu.addMenu(shortcutfinger.home3("Set")))
        add_ui_action(note_set_menu, shortcutfinger.home1("Meaning"), lambda _menu_string=menu_string: vocab.set_user_answer(_menu_string)) # type: ignore
        add_ui_action(note_set_menu, shortcutfinger.home2("Derived from"), lambda _menu_string=menu_string: vocab.set_related_derived_from(_menu_string)) # type: ignore
        add_ui_action(note_set_menu, shortcutfinger.home3("Ergative twin"), lambda _menu_string=menu_string: vocab.set_related_ergative_twin(_menu_string)) # type: ignore

    add_ui_action(note_menu, shortcutfinger.up1("Generate answer"), lambda: vocab.generate_and_set_answer())
    if vocab.can_generate_sentences_from_context_sentences(require_audio=False):
        add_ui_action(note_menu, shortcutfinger.up2("Generate sentences"), lambda: vocab.generate_sentences_from_context_sentences(require_audio=False))

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())
