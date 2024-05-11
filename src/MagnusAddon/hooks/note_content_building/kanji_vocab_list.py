from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.vocabnote import VocabNote
from sysutils import kana_utils
from sysutils.ex_str import newline

def sort_vocab_list(note: KanjiNote, primary_voc: list[str], vocabs: list[VocabNote]) -> None:
    def prefer_primary_vocab_in_order(local_vocab: VocabNote) -> int:
        for index, primary in enumerate(primary_voc):
            if local_vocab.get_question() == primary or local_vocab.get_readings()[0] == primary:
                return index

        return 100

    def prefer_more_studying_sentences(local_vocab: VocabNote) -> int:
        return -len(local_vocab.get_sentences_studying())

    def prefer_more_sentences(local_vocab: VocabNote) -> int:
        return -len(local_vocab.get_sentences())

    def prefer_non_compound(local_vocab: VocabNote) -> str:
        return "A" if kana_utils.is_only_kana(local_vocab.get_question()[1:]) else "B"

    def prefer_starts_with_kanji(local_vocab: VocabNote) -> str:
        return "A" if local_vocab.get_question()[0] == note.get_question() else "B"

    def prefer_high_priority(_vocab: VocabNote) -> int:
        return _vocab.priority_spec().priority

    vocabs.sort(key=lambda local_vocab: (prefer_primary_vocab_in_order(local_vocab),
                                         prefer_more_studying_sentences(local_vocab),
                                         prefer_more_sentences(local_vocab),
                                         prefer_high_priority(local_vocab),
                                         prefer_non_compound(local_vocab),
                                         prefer_starts_with_kanji(local_vocab),
                                         local_vocab.get_question()))

def _create_classes(_kanji: KanjiNote, _vocab: VocabNote) -> str:
    tags = list(_vocab.priority_spec().tags)
    tags.sort()
    classes = " ".join([f"""common_ness_{prio}""" for prio in tags])
    classes += f""" {_vocab.priority_spec().priority_string}"""
    if _vocab.get_question() in _kanji.get_primary_vocab() or _vocab.get_readings()[0] in _kanji.get_primary_vocab():
        classes += " primary_vocab"

    return classes

def generate_vocab_html_list(_kanji_note: KanjiNote, vocabs: list[VocabNote]) -> str:
    primary_voc = _kanji_note.get_primary_vocab()
    sort_vocab_list(_kanji_note, primary_voc, vocabs)

    return f'''
            <div class="kanjiVocabList">
                <div>

                {newline.join([f"""
                <div class="kanjiVocabEntry {_create_classes(_kanji_note, _vocab_note)}">
                    <span class="kanji clipboard">{_vocab_note.get_question()}</span>
                    (<span class="clipboard vocabReading">{_kanji_note.tag_readings_in_string(", ".join(_vocab_note.get_readings()), lambda read: f'<span class="kanjiReading">{read}</span>')}</span>)
                    {_vocab_note.get_meta_tags()}
                    <span class="meaning"> {_vocab_note.get_answer()}</span>
                </div>
                """ for _vocab_note in vocabs])}

                </div>
            </div>
            '''

def render_vocab_html_list(html: str, card: Card, _type_of_display: str) -> str:
    kanji_note = JPNote.note_from_card(card)

    if isinstance(kanji_note, KanjiNote):
        vocab_list = app.col().vocab.with_kanji(kanji_note)
        vocab_list_html = generate_vocab_html_list(kanji_note, vocab_list)
        html = html.replace("##VOCAB_LIST##", vocab_list_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_vocab_html_list)
