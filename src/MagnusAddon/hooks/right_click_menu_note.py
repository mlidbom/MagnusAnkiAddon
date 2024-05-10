from aqt.webview import AnkiWebView
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

def setup_note_menu(note: JPNote, root_menu: QMenu, sel_clip: str, selection: str, view: AnkiWebView) -> None:
    if sel_clip:
        add_lookup_action(root_menu, "&Open", su.lookup_text_object(sel_clip))

    note_menu: QMenu = checked_cast(QMenu, root_menu.addMenu("&Note"))
    note_lookup_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Lookup"))
    note_set_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Set"))
    note_hide_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Hide/Remove"))
    note_restore_menu: QMenu = checked_cast(QMenu, note_menu.addMenu("&Restore"))

    vocab_menu: QMenu = checked_cast(QMenu, root_menu.addMenu("&Vocab"))

    if sel_clip:
        add_vocab_menu = checked_cast(QMenu, vocab_menu.addMenu("&Set"))
        add_ui_action(add_vocab_menu, "&1", lambda: note.set_field(MyNoteFields.Vocab1, sel_clip))
        add_ui_action(add_vocab_menu, "&2", lambda: note.set_field(MyNoteFields.Vocab2, sel_clip))
        add_ui_action(add_vocab_menu, "&3", lambda: note.set_field(MyNoteFields.Vocab3, sel_clip))
        add_ui_action(add_vocab_menu, "&4", lambda: note.set_field(MyNoteFields.Vocab4, sel_clip))
        add_ui_action(add_vocab_menu, "&5", lambda: note.set_field(MyNoteFields.Vocab5, sel_clip))

    remove_vocab_menu = checked_cast(QMenu, vocab_menu.addMenu("&Remove"))
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
        sentence_note = checked_cast(SentenceNote, note)
        add_lookup_action(note_lookup_menu, "&Vocabulary words", su.notes_by_id([voc.get_id() for voc in note.ud_extract_vocab()]))
        add_lookup_action(note_lookup_menu, "&Kanji", f"""note:{NoteTypes.Kanji} ({" OR ".join([f"{NoteFields.Kanji.question}:{kan}" for kan in note.extract_kanji()])})""")

        if sel_clip:
            add_ui_action(note_hide_menu, "&Exclude vocab", lambda: sentence_note.exclude_vocab( sel_clip))

            highlighted_vocab_menu: QMenu = checked_cast(QMenu, root_menu.addMenu("&Highlighted Vocab"))
            add_ui_action(highlighted_vocab_menu, "&Add", lambda: sentence_note.add_extra_vocab(sel_clip))
            add_ui_action(highlighted_vocab_menu, "&Remove", lambda: sentence_note.add_extra_vocab(sel_clip))

    if isinstance(note, RadicalNote):
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{NoteTypes.Kanji} ( {su.field_contains_word(NoteFields.Kanji.Radicals_Names, note.get_answer())} OR {su.field_contains_word(NoteFields.Kanji.Radicals_Icons_Names, note.get_answer())} )")

    if isinstance(note, KanjiNote):
        kanji = note
        add_lookup_action(note_lookup_menu, "&Vocabs", su.vocab_with_kanji(note))
        add_lookup_action(note_lookup_menu, "&Dependencies", su.notes_by_note(app.col().kanji.dependencies_of(kanji)))
        add_lookup_action(note_lookup_menu, "&Sentences", su.sentence_search(kanji.get_question(), exact=True))

        if not kanji.get_user_mnemonic():
            add_ui_action(note_hide_menu, "&Mnemonic", lambda: kanji.override_meaning_mnemonic())
        if kanji.get_user_mnemonic() == "-":
            add_ui_action(note_restore_menu, "&Mnemonic", lambda: kanji.restore_meaning_mnemonic())
        if not kanji.get_user_answer():
            add_ui_action(note_menu, "Accept &meaning", lambda: kanji.set_user_answer(format_kanji_meaning(kanji.get_answer())))

        if sel_clip:
            primary_vocab_menu: QMenu = checked_cast(QMenu, root_menu.addMenu("&Primary Vocab"))
            if sel_clip in kanji.get_primary_vocab():
                add_ui_action(primary_vocab_menu, "&Remove", lambda: kanji.remove_primary_vocab(sel_clip))
            else:
                add_ui_action(primary_vocab_menu, "&Add", lambda: kanji.add_primary_vocab(sel_clip))
            add_ui_action(primary_vocab_menu, "&Set", lambda: kanji.set_primary_vocab([sel_clip]))


    if isinstance(note, VocabNote):
        vocab = note
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{NoteTypes.Kanji} ( {' OR '.join([f'{NoteFields.Kanji.question}:{char}' for char in note.get_question()])} )")
        if vocab.get_related_ergative_twin():
            add_single_vocab_lookup_action(note_lookup_menu, "&Ergative twin", vocab.get_related_ergative_twin())

        add_lookup_action(note_lookup_menu, "&Sentence", su.sentence_search(vocab.get_question()))
        add_text_vocab_lookup(note_lookup_menu, "&Compounds", note.get_question())
        add_vocab_dependencies_lookup(note_lookup_menu, "&Dependencies", note)

        if not vocab.get_mnemonics_override():
            add_ui_action(note_hide_menu, "&Mnemonic", lambda: vocab.override_meaning_mnemonic())
        if vocab.get_mnemonics_override() == "-":
            add_ui_action(note_restore_menu, "&Mnemonic", lambda: vocab.restore_meaning_mnemonic())
        if not vocab.get_user_answer():
            add_ui_action(note_menu, "Accept &meaning", lambda: vocab.set_user_answer(format_vocab_meaning(vocab.get_answer())))

        add_ui_action(note_set_menu, "&Generate answer", lambda: vocab.generate_and_set_answer())
        add_ui_action(note_set_menu, "&Meaning", lambda: vocab.set_user_answer(sel_clip))
        add_ui_action(note_set_menu, "&Confused with", lambda: vocab.set_related_confused_with(sel_clip))
        add_ui_action(note_set_menu, "&Derived from", lambda: vocab.set_related_derived_from(sel_clip))
        add_ui_action(note_set_menu, "S&imilar meaning", lambda: vocab.set_related_similar_meaning(sel_clip))
        add_ui_action(note_set_menu, "&Ergative twin", lambda: vocab.set_related_ergative_twin(sel_clip))

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())

def format_kanji_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning.lower().replace(", ", "/").replace(" ", "-"))
