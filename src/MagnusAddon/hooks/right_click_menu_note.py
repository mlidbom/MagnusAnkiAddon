from aqt.webview import AnkiWebView

from hooks.right_click_menu_utils import add_ui_action, add_kanji_primary_vocab, set_kanji_primary_vocab, add_sentence_lookup, add_lookup_action
from note.wanikanjinote import WaniKanjiNote
from note.waniradicalnote import WaniRadicalNote
from note.wanivocabnote import WaniVocabNote
from sysutils import kana_utils
from wanikani.wani_constants import MyNoteFields, Wani


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
    if isinstance(note, WaniRadicalNote):
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} {Wani.KanjiFields.Radicals_Names}:re:\\b{note.get_radical_name()}\\b")
    if isinstance(note, WaniKanjiNote):
        kanji = note
        add_lookup_action(note_lookup_menu, "&Vocabs", f"deck:*Vocab* deck:*Read* (Vocab:*{note.get_kanji()}*)")
        radicals = [rad.strip() for rad in note.get_radicals_names().split(",")]
        radicals_clause = " OR ".join([f"{Wani.RadicalFields.Radical_Name}:{rad}" for rad in radicals])
        add_lookup_action(note_lookup_menu, "&Radicals", f"note:{Wani.NoteType.Radical} ({radicals_clause})")

        if not kanji.get_mnemonics_override():
            add_ui_action(note_menu, "&Hide mnemonic", lambda: kanji.override_meaning_mnemonic())
        if kanji.get_mnemonics_override() == "-":
            add_ui_action(note_menu, "&Restore mnemonic", lambda: kanji.restore_meaning_mnemonic())
        if not kanji.get_override_meaning():
            add_ui_action(note_menu, "&Accept meaning", lambda: kanji.set_override_meaning(kanji.get_kanji_meaning().lower().replace(", ", "/").replace(" ", "-")))

        if selection:
            add_ui_action(note_add_menu, "&Primary vocab", lambda: add_kanji_primary_vocab(kanji, selection, view))
            add_ui_action(note_set_menu, "&Primary vocab", lambda: set_kanji_primary_vocab(kanji, selection, view))
    if isinstance(note, WaniVocabNote):
        vocab = note
        add_lookup_action(note_lookup_menu, "&Kanji", f"note:{Wani.NoteType.Kanji} ( {' OR '.join([f'{Wani.KanjiFields.Kanji}:{char}' for char in note.get_vocab()])} )")
        add_sentence_lookup(note_lookup_menu, "&Sentence", kana_utils.get_conjugation_base(vocab.get_vocab()))

        if not vocab.get_mnemonics_override():
            add_ui_action(note_menu, "&Hide mnemonic", lambda: vocab.override_meaning_mnemonic())
        if vocab.get_mnemonics_override() == "-":
            add_ui_action(note_menu, "&Restore mnemonic", lambda: vocab.restore_meaning_mnemonic())
        if not vocab.get_override_meaning():
            add_ui_action(note_menu, "Accept &meaning", lambda: vocab.set_override_meaning(vocab.get_vocab_meaning().lower().replace(", ", "/").replace(" ", "-")))

        add_ui_action(note_set_menu, "&Meaning", lambda: vocab.set_override_meaning(sel_clip))
        add_ui_action(note_set_menu, "&Similar vocab", lambda: vocab.set_related_similar_vocab(sel_clip))
        add_ui_action(note_set_menu, "&Derived from", lambda: vocab.set_related_derived_from(sel_clip))
        add_ui_action(note_set_menu, "S&imilar meaning", lambda: vocab.set_related_similar_meaning(sel_clip))
        add_ui_action(note_set_menu, "&Homophone", lambda: vocab.set_related_homophones(sel_clip))
        add_ui_action(note_set_menu, "&Ergative twin", lambda: vocab.set_related_ergative_twin(sel_clip))
