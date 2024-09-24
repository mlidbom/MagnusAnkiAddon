from PyQt6.QtWidgets import QMenu

from ankiutils import app, query_builder as su
from hooks.right_click_menu_utils import add_lookup_action, add_single_vocab_lookup_action, add_text_vocab_lookup, add_ui_action, add_vocab_dependencies_lookup
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.note_constants import MyNoteFields, NoteFields, NoteTypes
from note.radicalnote import RadicalNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_str
from sysutils.typed import checked_cast

def setup_note_menu(note: JPNote, root_menu: QMenu, string_menus: list[tuple[QMenu, str]]) -> None:
    note_menu: QMenu
    note_lookup_menu: QMenu
    note_hide_menu: QMenu

    def setup_vocab_menu() -> None:
        for _string_menu, _menu_string in string_menus:
            vocab_menu: QMenu = checked_cast(QMenu, _string_menu.addMenu("&Vocab"))
            add_vocab_menu = checked_cast(QMenu, vocab_menu.addMenu("&Set"))
            add_ui_action(add_vocab_menu, "&1", lambda: note.set_field(MyNoteFields.Vocab1, _menu_string))
            add_ui_action(add_vocab_menu, "&2", lambda: note.set_field(MyNoteFields.Vocab2, _menu_string))
            add_ui_action(add_vocab_menu, "&3", lambda: note.set_field(MyNoteFields.Vocab3, _menu_string))
            add_ui_action(add_vocab_menu, "&4", lambda: note.set_field(MyNoteFields.Vocab4, _menu_string))
            add_ui_action(add_vocab_menu, "&5", lambda: note.set_field(MyNoteFields.Vocab5, _menu_string))

        if note.get_field(MyNoteFields.Vocab1) or note.get_field(MyNoteFields.Vocab2) or note.get_field(MyNoteFields.Vocab3) or note.get_field(MyNoteFields.Vocab4) or note.get_field(MyNoteFields.Vocab5):
            remove_vocab_menu = checked_cast(QMenu, root_menu.addMenu("&Remove vocab"))
            add_ui_action(remove_vocab_menu, "&1", lambda: note.set_field(MyNoteFields.Vocab1, ""))
            add_ui_action(remove_vocab_menu, "&2", lambda: note.set_field(MyNoteFields.Vocab2, ""))
            add_ui_action(remove_vocab_menu, "&3", lambda: note.set_field(MyNoteFields.Vocab3, ""))
            add_ui_action(remove_vocab_menu, "&4", lambda: note.set_field(MyNoteFields.Vocab4, ""))
            add_ui_action(remove_vocab_menu, "&5", lambda: note.set_field(MyNoteFields.Vocab5, ""))

            def clear_all_vocabs() -> None:
                for field in [MyNoteFields.Vocab1, MyNoteFields.Vocab2, MyNoteFields.Vocab3, MyNoteFields.Vocab4, MyNoteFields.Vocab5]:
                    note.set_field(field, "")

            add_ui_action(remove_vocab_menu, "&All", clear_all_vocabs)

    if isinstance(note, SentenceNote):
        note_menu = checked_cast(QMenu, root_menu.addMenu("&Note"))
        note_lookup_menu = checked_cast(QMenu, note_menu.addMenu("&Open"))

        sentence_note = checked_cast(SentenceNote, note)
        add_lookup_action(note_lookup_menu, "Highlighted &Vocab", su.vocabs_lookup_strings(note.get_user_extra_vocab()))
        add_lookup_action(note_lookup_menu, "&Kanji", f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in note.extract_kanji()])})""")
        add_lookup_action(note_lookup_menu, "&Parsed words", su.notes_by_id([voc.get_id() for voc in note.ud_extract_vocab()]))

        def position_vocab_menu(_menu:QMenu, _vocab_to_add: str, _title: str) -> None:
            highlighted_vocab_menu: QMenu = checked_cast(QMenu, _menu.addMenu(_title))
            for index, _vocab in enumerate(sentence_note.get_user_extra_vocab()):
                add_ui_action(highlighted_vocab_menu, f"&{index + 1}. {_vocab}", lambda _index=index: sentence_note.position_extra_vocab(_vocab_to_add, _index))  # type: ignore

            add_ui_action(highlighted_vocab_menu, f"[&Last]", lambda: sentence_note.position_extra_vocab(_vocab_to_add))

            if menu_string in sentence_note.get_user_extra_vocab():
                add_ui_action(highlighted_vocab_menu, "&Remove", lambda _menu_string=menu_string: sentence_note.remove_extra_vocab(_menu_string)) # type: ignore

        for string_menu, menu_string in string_menus:
            position_vocab_menu(string_menu, menu_string, "H&ighlighted Vocab")
            add_ui_action(string_menu, "&Exclude vocab", lambda _menu_string=menu_string: sentence_note.exclude_vocab(_menu_string)) # type: ignore

        position_vocab_menu(note_menu, "-", "&Highlighted Vocab Separator")

        setup_vocab_menu()

    if isinstance(note, RadicalNote):
        note_menu = checked_cast(QMenu, root_menu.addMenu("&Note"))
        note_lookup_menu = checked_cast(QMenu, note_menu.addMenu("&Open"))
        add_lookup_action(note_lookup_menu, "&Kanji", su.kanji_with_radical(note))

    if isinstance(note, KanjiNote):
        note_menu = checked_cast(QMenu, root_menu.addMenu("&Note"))
        note_lookup_menu = checked_cast(QMenu, note_menu.addMenu("&Open"))

        kanji = note
        add_lookup_action(note_lookup_menu, "&Primary Vocabs", su.vocabs_lookup_strings(note.get_primary_vocab()))
        add_lookup_action(note_lookup_menu, "&Vocabs", su.vocab_with_kanji(note))
        add_lookup_action(note_lookup_menu, "&Radicals", su.notes_by_note(app.col().kanji.dependencies_of(kanji)))
        add_lookup_action(note_lookup_menu, "&Kanji", su.kanji_with_kanji_radical(note))
        add_lookup_action(note_lookup_menu, "&Sentences", su.sentence_search(kanji.get_question(), exact=True))

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
            primary_vocab_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("&Primary Vocab"))
            if menu_string in kanji.get_primary_vocab():
                add_ui_action(primary_vocab_menu, "&Remove", lambda _menu_string=menu_string: kanji.remove_primary_vocab(_menu_string)) # type: ignore
            else:
                add_ui_action(primary_vocab_menu, "&Add", lambda _menu_string=menu_string: kanji.add_primary_vocab(_menu_string)) # type: ignore

            kanji_add_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("&Add"))
            add_ui_action(kanji_add_menu, "&Similar meaning", lambda _menu_string=menu_string: kanji.add_user_similar_meaning(_menu_string)) # type: ignore


    if isinstance(note, VocabNote):
        vocab = note
        setup_vocab_menu()

        note_menu = checked_cast(QMenu, root_menu.addMenu("&Note"))
        note_lookup_menu = checked_cast(QMenu, note_menu.addMenu("&Open"))
        note_hide_menu = checked_cast(QMenu, note_menu.addMenu("&Hide/Remove"))
        note_restore_menu = checked_cast(QMenu, note_menu.addMenu("&Restore"))

        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{NoteTypes.Kanji} ( {' OR '.join([f'{NoteFields.Kanji.question}:{char}' for char in note.get_question()])} )")
        if vocab.get_related_ergative_twin():
            add_single_vocab_lookup_action(note_lookup_menu, "Ergative &twin", vocab.get_related_ergative_twin())

        add_lookup_action(note_lookup_menu, "&Sentences I'm Studying", su.notes_lookup(vocab.get_sentences_studying()))
        add_lookup_action(note_lookup_menu, "S&entences", su.sentence_search(vocab.get_question()))

        add_text_vocab_lookup(note_lookup_menu, "&Compounds", note.get_question())
        add_vocab_dependencies_lookup(note_lookup_menu, "&Dependencies", note)

        for reading in note.get_readings():
            add_lookup_action(note_lookup_menu, f"&Homonyms: {reading}", su.notes_lookup(app.col().vocab.with_reading(reading)))

        if not vocab.get_mnemonics_override():
            add_ui_action(note_hide_menu, "&Mnemonic", lambda: vocab.override_meaning_mnemonic())
        if vocab.get_mnemonics_override() == "-":
            add_ui_action(note_restore_menu, "&Mnemonic", lambda: vocab.restore_meaning_mnemonic())
        if not vocab.get_user_answer():
            add_ui_action(note_menu, "Accept &meaning", lambda: vocab.set_user_answer(format_vocab_meaning(vocab.get_answer())))

        for string_menu, menu_string in string_menus:
            vocab_add_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("&Add"))
            add_ui_action(vocab_add_menu, "S&imilar meaning", lambda _menu_string=menu_string: vocab.add_related_similar_meaning(_menu_string)) # type: ignore

        for string_menu, menu_string in string_menus:
            note_set_menu: QMenu = checked_cast(QMenu, string_menu.addMenu("&Set"))
            add_ui_action(note_set_menu, "&Meaning", lambda _menu_string=menu_string: vocab.set_user_answer(_menu_string)) # type: ignore
            add_ui_action(note_set_menu, "&Confused with", lambda _menu_string=menu_string: vocab.set_related_confused_with(_menu_string)) # type: ignore
            add_ui_action(note_set_menu, "&Derived from", lambda _menu_string=menu_string: vocab.set_related_derived_from(_menu_string)) # type: ignore
            add_ui_action(note_set_menu, "&Ergative twin", lambda _menu_string=menu_string: vocab.set_related_ergative_twin(_menu_string)) # type: ignore

        add_ui_action(note_menu, "&Generate answer", lambda: vocab.generate_and_set_answer())

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())

def format_kanji_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.lower().replace(", ", "/").replace(" ", "-"))
