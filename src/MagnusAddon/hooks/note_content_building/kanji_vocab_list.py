from anki.cards import Card
from aqt import gui_hooks

from ankiutils import query_builder
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.vocabnote import VocabNote
from sysutils import kana_utils
from sysutils.stringutils import StringUtils
from ankiutils import app


def sort_vocab_list(note:KanjiNote, primary_voc: list[str], vocabs: list[VocabNote]) -> None:
    def prefer_primary_vocab_in_order(local_vocab: VocabNote) -> int:
        for index, primary in enumerate(primary_voc):
            if local_vocab.get_question() == primary or local_vocab.get_readings()[0] == primary:
                return index

        return 100

    def prefer_non_compound(local_vocab: VocabNote) -> str:
        return "A" if kana_utils.is_only_kana(local_vocab.get_question()[1:]) else "B"

    def prefer_starts_with_vocab(local_vocab: VocabNote) -> str:
        return "A" if local_vocab.get_question()[0] == note.get_question() else "B"

    vocabs.sort(key=lambda local_vocab: (prefer_primary_vocab_in_order(local_vocab),
                                         prefer_non_compound(local_vocab),
                                         prefer_starts_with_vocab(local_vocab),
                                         local_vocab.get_question()))

def generate_vocab_html_list(note: KanjiNote, vocabs: list[VocabNote]) -> str:
    primary_voc = note.get_primary_vocab()
    sort_vocab_list(note, primary_voc, vocabs)

    return f'''
            <div class="kanjiVocabList">
                <div>

                {StringUtils.newline().join([f"""
                <div class="kanjiVocabEntry">
                    <span class="kanji clipboard">{inner_vocab.get_question()}</span>
                    (<span class="clipboard vocabReading">{note.tag_readings_in_string(", ".join(inner_vocab.get_readings()), lambda read: f'<span class="kanjiReading">{read}</span>')}</span>)
                    <span class="meaning"> {StringUtils.strip_html_markup(inner_vocab.get_active_answer())}</span>
                </div>
                """ for inner_vocab in vocabs])}

                </div>
            </div>
            '''

def render_vocab_html_list(html:str, card: Card, _type_of_display:str) -> str:
    kanji_note = JPNote.note_from_card(card)

    if isinstance(kanji_note, KanjiNote):
        vocab_list = app.col().vocab.search(query_builder.vocab_with_kanji(kanji_note))
        vocab_list_html = generate_vocab_html_list(kanji_note, vocab_list)
        html = html.replace("##VOCAB_LIST##", vocab_list_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_vocab_html_list)