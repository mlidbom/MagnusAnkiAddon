from PyQt6.QtWidgets import QMenu

from ankiutils import app, query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_single_vocab_lookup_action, add_text_vocab_lookup, add_ui_action, add_vocab_dependencies_lookup
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import NoteFields, NoteTypes
from note.radicalnote import RadicalNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_str
from sysutils.typed import checked_cast

def setup_note_menu(note: JPNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_lookup_menu: QMenu
    note_hide_menu: QMenu

    if isinstance(note, SentenceNote):
        note_lookup_menu = checked_cast(QMenu, note_menu.addMenu("&Open"))

        sentence_note = checked_cast(SentenceNote, note)
        add_lookup_action(note_lookup_menu, "Highlighted V&ocab", query_builder.vocabs_lookup_strings(note.get_user_highlighted_vocab()))
        add_lookup_action(note_lookup_menu, "Highlighted Vocab Read C&ard", query_builder.vocabs_lookup_strings_read_card(note.get_user_highlighted_vocab()))
        add_lookup_action(note_lookup_menu, "&Kanji", f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in note.extract_kanji()])})""")
        add_lookup_action(note_lookup_menu, "&Parsed words", query_builder.notes_by_id([voc.get_id() for voc in note.ud_extract_vocab()]))

        def position_vocab_menu(_menu:QMenu, _vocab_to_add: str, _title: str) -> None:
            highlighted_vocab_menu: QMenu = checked_cast(QMenu, _menu.addMenu(_title))
            for index, _vocab in enumerate(sentence_note.get_user_highlighted_vocab()):
                add_ui_action(highlighted_vocab_menu, f"&{index + 1}. {_vocab}", lambda _index=index: sentence_note.position_extra_vocab(_vocab_to_add, _index))  # type: ignore

            add_ui_action(highlighted_vocab_menu, f"[L&ast]", lambda: sentence_note.position_extra_vocab(_vocab_to_add))

            if _vocab_to_add in sentence_note.get_user_highlighted_vocab():
                add_ui_action(highlighted_vocab_menu, "R&emove", lambda __vocab_to_add=_vocab_to_add: sentence_note.remove_extra_vocab(__vocab_to_add)) # type: ignore

        for string_menu, menu_string in string_menus:
            position_vocab_menu(string_menu, menu_string, "H&ighlighted Vocab")
            add_ui_action(string_menu, "E&xclude vocab", lambda _menu_string=menu_string: sentence_note.exclude_vocab(_menu_string)) # type: ignore

        position_vocab_menu(note_menu, "-", "H&ighlighted Vocab Separator")

    if isinstance(note, RadicalNote):
        note_lookup_menu = checked_cast(QMenu, note_menu.addMenu("&Open"))
        add_lookup_action(note_lookup_menu, "&Kanji", query_builder.kanji_with_radical(note))

    if isinstance(note, KanjiNote):
        note_lookup_menu = checked_cast(QMenu, note_menu.addMenu("&Open"))

        kanji = note
        add_lookup_action(note_lookup_menu, "Primary Vocabs", query_builder.vocabs_lookup_strings(note.get_primary_vocab()))
        add_lookup_action(note_lookup_menu, "&Vocabs", query_builder.vocab_with_kanji(note))
        add_lookup_action(note_lookup_menu, "&Radicals", query_builder.notes_by_note(app.col().kanji.dependencies_of(kanji)))
        add_lookup_action(note_lookup_menu, "&Kanji", query_builder.kanji_with_kanji_radical(note))
        add_lookup_action(note_lookup_menu, "&Sentences", query_builder.sentence_search(kanji.get_question(), exact=True))

        if not kanji.get_user_mnemonic():
            note_hide_menu = checked_cast(QMenu, note_menu.addMenu("&Hide/Remove"))
            add_ui_action(note_hide_menu, "&Mnemonic", lambda: kanji.override_meaning_mnemonic())
        if kanji.get_user_mnemonic() == "-":
            note_restore_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Restore"))
            add_ui_action(note_restore_menu, "&Mnemonic", lambda: kanji.restore_meaning_mnemonic())
        if not kanji.get_user_answer():
            add_ui_action(note_menu, "Accept &meaning", lambda: kanji.set_user_answer(format_kanji_meaning(kanji.get_answer())))

        add_ui_action(note_menu, "Reset Primary Vocabs", lambda: kanji.set_primary_vocab([]))

        for string_menu, menu_string in string_menus:
            primary_vocab_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("Pr&imary Vocab"))
            if menu_string in kanji.get_primary_vocab():
                add_ui_action(primary_vocab_menu, "R&emove", lambda _menu_string=menu_string: kanji.remove_primary_vocab(_menu_string)) # type: ignore
            else:
                add_ui_action(primary_vocab_menu, "&Add", lambda _menu_string=menu_string: kanji.add_primary_vocab(_menu_string)) # type: ignore

            kanji_add_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("&Add"))
            add_ui_action(kanji_add_menu, "&Similar meaning", lambda _menu_string=menu_string: kanji.add_user_similar_meaning(_menu_string)) # type: ignore


    if isinstance(note, VocabNote):
        vocab = note

        note_lookup_menu = checked_cast(QMenu, note_menu.addMenu("&Open"))
        note_hide_menu = checked_cast(QMenu, note_menu.addMenu("&Hide/Remove"))
        note_restore_menu = checked_cast(QMenu, note_menu.addMenu("&Restore"))

        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{NoteTypes.Kanji} ( {' OR '.join([f'{NoteFields.Kanji.question}:{char}' for char in note.get_question()])} )")
        if vocab.get_related_ergative_twin():
            add_single_vocab_lookup_action(note_lookup_menu, "Ergative &twin", vocab.get_related_ergative_twin())

        add_lookup_action(note_lookup_menu, "S&entences I'm Studying", query_builder.notes_lookup(vocab.get_sentences_studying()))
        add_lookup_action(note_lookup_menu, "&Sentences", query_builder.notes_lookup(vocab.get_sentences()))
        add_lookup_action(note_lookup_menu, "Sentences with &primary form", query_builder.notes_lookup(vocab.get_sentences_with_primary_form()))

        add_text_vocab_lookup(note_lookup_menu, "&Compounds", note.get_question())
        add_vocab_dependencies_lookup(note_lookup_menu, "&Dependencies", note)

        for reading in note.get_readings():
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


        add_ui_action(note_menu, "&Generate answer", lambda: vocab.generate_and_set_answer())
        if vocab.can_generate_sentences_from_context_sentences(require_audio=False):
            add_ui_action(note_menu, "&Generate sentences", lambda: vocab.generate_sentences_from_context_sentences(require_audio=False))

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())

def format_kanji_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.lower().replace(", ", "/").replace(" ", "-"))
