from aqt.webview import AnkiWebView

from batches import local_note_updater
from hooks.right_click_menu_utils import add_ui_action, add_lookup_action, add_sentence_lookup
from note.sentencenote import SentenceNote
from note.wanikanjinote import WaniKanjiNote
from note.waniradicalnote import WaniRadicalNote
from note.wanivocabnote import WaniVocabNote
from sysutils.utils import StringUtils
from wanikani.wani_constants import MyNoteFields, Wani, SentenceNoteFields


def setup_note_menu(note, root_menu, sel_clip, selection, view: AnkiWebView):
    note_menu = root_menu.addMenu("&Note")
    note_lookup_menu = note_menu.addMenu("&Lookup")
    note_add_menu = note_menu.addMenu("&Add")
    note_set_menu = note_menu.addMenu("&Set")

    if sel_clip:
        add_vocab_menu = note_add_menu.addMenu("&Vocab")
        add_ui_action(add_vocab_menu, "&1", lambda: note.set_field(MyNoteFields.Vocab1, sel_clip))
        add_ui_action(add_vocab_menu, "&2", lambda: note.set_field(MyNoteFields.Vocab2, sel_clip))
        add_ui_action(add_vocab_menu, "&3", lambda: note.set_field(MyNoteFields.Vocab3, sel_clip))
        add_ui_action(add_vocab_menu, "&4", lambda: note.set_field(MyNoteFields.Vocab4, sel_clip))
        add_ui_action(add_vocab_menu, "&5", lambda: note.set_field(MyNoteFields.Vocab5, sel_clip))

    if isinstance(note, SentenceNote):
        def voc_clause(voc:str) -> str: return f'Vocab:re:\\b{voc}\\b OR Reading:re:\\b{voc}\\b'
        add_lookup_action(note_lookup_menu,
                          "&Vocabulary words",
                          f"deck:*Vocab* deck:*Read* ({' OR '.join([voc_clause(voc) for voc in note.parse_words_from_expression()])})")

    if isinstance(note, WaniRadicalNote):
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} {Wani.KanjiFields.Radicals_Names}:re:\\b{note.get_radical_name()}\\b")
    if isinstance(note, WaniKanjiNote):
        kanji = note
        add_lookup_action(note_lookup_menu, "&Vocabs", f"deck:*Vocab* deck:*Read* (Vocab:*{note.get_kanji()}*)")
        radicals = [rad.strip() for rad in note.get_radicals_names().split(",")]
        radicals_clause = " OR ".join([f"{Wani.RadicalFields.Radical_Name}:{rad}" for rad in radicals])
        add_lookup_action(note_lookup_menu, "&Radicals", f"note:{Wani.NoteType.Radical} ({radicals_clause})")
        add_sentence_lookup(note_lookup_menu, "&Sentences", sel_clip)

        if not kanji.get_mnemonics_override():
            add_ui_action(note_menu, "&Hide mnemonic", lambda: kanji.override_meaning_mnemonic())
        if kanji.get_mnemonics_override() == "-":
            add_ui_action(note_menu, "&Restore mnemonic", lambda: kanji.restore_meaning_mnemonic())
        if not kanji.get_override_meaning():
            add_ui_action(note_menu, "Accept &meaning", lambda: kanji.set_override_meaning(format_kanji_meaning(kanji.get_kanji_meaning())))

        if selection:
            add_ui_action(note_add_menu, "&Primary vocab", lambda: add_kanji_primary_vocab(kanji, selection, view))
            add_ui_action(note_set_menu, "&Primary vocab", lambda: set_kanji_primary_vocab(kanji, selection, view))
    if isinstance(note, WaniVocabNote):
        vocab = note
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.Kanji}:{char}' for char in note.get_vocab()])} )")
        add_lookup_action(note_lookup_menu, "&Sentence", f"(deck:*sentence* deck:*listen*) ({SentenceNoteFields.ParsedWords}:re:\\b{note.get_vocab()}\\b OR Expression:*{note.get_vocab()}*)")

        if not vocab.get_mnemonics_override():
            add_ui_action(note_menu, "&Hide mnemonic", lambda: vocab.override_meaning_mnemonic())
        if vocab.get_mnemonics_override() == "-":
            add_ui_action(note_menu, "&Restore mnemonic", lambda: vocab.restore_meaning_mnemonic())
        if not vocab.get_override_meaning():
            add_ui_action(note_menu, "Accept &meaning", lambda: vocab.set_override_meaning(format_vocab_meaning(vocab.get_vocab_meaning())))

        add_ui_action(note_set_menu, "&Meaning", lambda: vocab.set_override_meaning(sel_clip))
        add_ui_action(note_set_menu, "&Similar vocab", lambda: vocab.set_related_similar_vocab(sel_clip))
        add_ui_action(note_set_menu, "&Derived from", lambda: vocab.set_related_derived_from(sel_clip))
        add_ui_action(note_set_menu, "S&imilar meaning", lambda: vocab.set_related_similar_meaning(sel_clip))
        add_ui_action(note_set_menu, "&Homophone", lambda: vocab.set_related_homophones(sel_clip))
        add_ui_action(note_set_menu, "&Ergative twin", lambda: vocab.set_related_ergative_twin(sel_clip))


def add_kanji_primary_vocab(note: WaniKanjiNote, selection: str, _view: AnkiWebView):
    primary_vocabs = [voc for voc in [note.get_primary_vocab(), note.tag_readings_in_string(selection, lambda read: f"<read>{read}</read>")] if voc]
    note.set_primary_vocab(", ".join(primary_vocabs))
    local_note_updater.update_kanji(note)


def set_kanji_primary_vocab(note: WaniKanjiNote, selection: str, view: AnkiWebView):
    note.set_primary_vocab("")
    add_kanji_primary_vocab(note, selection, view)

def format_vocab_meaning(meaning:str) -> str:
    return StringUtils.strip_markup(meaning.lower().replace(", ", "/"))

def format_kanji_meaning(meaning:str) -> str:
    return StringUtils.strip_markup(meaning.lower().replace(", ", "/").replace(" ", "-"))
