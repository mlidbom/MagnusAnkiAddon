from aqt.webview import AnkiWebView

from batches import local_note_updater
from hooks.right_click_menu_utils import add_ui_action, add_lookup_action, add_sentence_lookup, add_single_vocab_lookup_action, add_text_vocab_lookup, add_vocab_dependencies_lookup
from note.sentencenote import SentenceNote
from note.wanikanjinote import WaniKanjiNote
from note.waniradicalnote import WaniRadicalNote
from note.wanivocabnote import WaniVocabNote
from sysutils.utils import StringUtils
from wanikani.wani_constants import MyNoteFields, Wani, SentenceNoteFields
from ankiutils import search_utils as su

def setup_note_menu(note, root_menu, sel_clip, selection, view: AnkiWebView):
    note_menu = root_menu.addMenu("&Note")
    note_lookup_menu = note_menu.addMenu("&Lookup")
    note_add_menu = note_menu.addMenu("&Add")
    note_set_menu = note_menu.addMenu("&Set")
    note_hide_menu = note_menu.addMenu("&Hide")
    note_restore_menu = note_menu.addMenu("&Restore")

    if sel_clip:
        add_vocab_menu = note_set_menu.addMenu("&Vocab")
        add_ui_action(add_vocab_menu, "&1", lambda: note.set_field(MyNoteFields.Vocab1, sel_clip))
        add_ui_action(add_vocab_menu, "&2", lambda: note.set_field(MyNoteFields.Vocab2, sel_clip))
        add_ui_action(add_vocab_menu, "&3", lambda: note.set_field(MyNoteFields.Vocab3, sel_clip))
        add_ui_action(add_vocab_menu, "&4", lambda: note.set_field(MyNoteFields.Vocab4, sel_clip))
        add_ui_action(add_vocab_menu, "&5", lambda: note.set_field(MyNoteFields.Vocab5, sel_clip))

    if isinstance(note, SentenceNote):
        add_text_vocab_lookup(note_lookup_menu, "&Vocabulary words", note.get_active_question())
        add_lookup_action(note_lookup_menu, "&Kanji", f"""note:{Wani.NoteType.Kanji} ({" OR ".join([f"{Wani.KanjiFields.question}:{kan}" for kan in note.extract_kanji()])})""")

    if isinstance(note, WaniRadicalNote):
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} {Wani.KanjiFields.Radicals_Names}:re:\\b{note.get_a()}\\b")

    if isinstance(note, WaniKanjiNote):
        kanji = note
        add_lookup_action(note_lookup_menu, "&Vocabs", f"{su.vocab_read} (Q:*{note.get_question()}*)")
        radicals = [rad.strip() for rad in note.get_radicals_names().split(",")]
        radicals_clause = " OR ".join([f"{Wani.RadicalFields.answer}:{rad}" for rad in radicals])
        add_lookup_action(note_lookup_menu, "&Radicals", f"note:{Wani.NoteType.Radical} ({radicals_clause})")
        add_sentence_lookup(note_lookup_menu, "&Sentences", sel_clip)

        if not kanji.get_mnemonics_override():
            add_ui_action(note_hide_menu, "&Mnemonic", lambda: kanji.override_meaning_mnemonic())
        if kanji.get_mnemonics_override() == "-":
            add_ui_action(note_restore_menu, "&Mnemonic", lambda: kanji.restore_meaning_mnemonic())
        if not kanji.get_user_answer():
            add_ui_action(note_menu, "Accept &meaning", lambda: kanji.set_user_answer(format_kanji_meaning(kanji.get_active_answer())))

        if selection:
            add_ui_action(note_add_menu, "&Primary vocab", lambda: add_kanji_primary_vocab(kanji, selection, view))
            add_ui_action(note_set_menu, "&Primary vocab", lambda: set_kanji_primary_vocab(kanji, selection, view))

    if isinstance(note, WaniVocabNote):
        vocab = note
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.question}:{char}' for char in note.get_question()])} )")
        if vocab.get_related_ergative_twin():
            add_single_vocab_lookup_action(note_lookup_menu, "&Ergative twin", vocab.get_related_ergative_twin())

        add_lookup_action(note_lookup_menu, "&Sentence", f"(deck:*sentence* deck:*listen*) ({SentenceNoteFields.ParsedWords}:re:\\b{note.get_question()}\\b OR Q:*{note.get_question()}*)")
        add_text_vocab_lookup(note_lookup_menu, "&Compounds", note.get_question())
        add_vocab_dependencies_lookup(note_lookup_menu, "&Dependencies", note)

        if not vocab.get_mnemonics_override():
            add_ui_action(note_hide_menu, "&Mnemonic", lambda: vocab.override_meaning_mnemonic())
        if vocab.get_mnemonics_override() == "-":
            add_ui_action(note_restore_menu, "&Mnemonic", lambda: vocab.restore_meaning_mnemonic())
        if not vocab.get_user_answer():
            add_ui_action(note_menu, "Accept &meaning", lambda: vocab.set_user_answer(format_vocab_meaning(vocab.get_active_answer())))

        add_ui_action(note_set_menu, "&Meaning", lambda: vocab.set_user_answer(sel_clip))
        add_ui_action(note_set_menu, "&Similar vocab", lambda: vocab.set_related_similar_vocab(sel_clip))
        add_ui_action(note_set_menu, "&Derived from", lambda: vocab.set_related_derived_from(sel_clip))
        add_ui_action(note_set_menu, "S&imilar meaning", lambda: vocab.set_related_similar_meaning(sel_clip))
        add_ui_action(note_set_menu, "&Ergative twin", lambda: vocab.set_related_ergative_twin(sel_clip))


def add_kanji_primary_vocab(note: WaniKanjiNote, selection: str, _view: AnkiWebView):
    note.set_primary_vocab(note.get_primary_vocab() + [selection])
    local_note_updater.update_kanji(note)


def set_kanji_primary_vocab(note: WaniKanjiNote, selection: str, view: AnkiWebView):
    note.set_primary_vocab([])
    add_kanji_primary_vocab(note, selection, view)

def format_vocab_meaning(meaning:str) -> str:
    return StringUtils.strip_markup(meaning.lower().replace(", ", "/"))

def format_kanji_meaning(meaning:str) -> str:
    return StringUtils.strip_markup(meaning.lower().replace(", ", "/").replace(" ", "-"))
