from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app, ui_utils
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.vocabnote import VocabNote
from sysutils import ex_str, kana_utils


def render_compound_list(html: str, card: Card, _type_of_display: str) -> str:
    vocab_note = JPNote.note_from_note(card.note())
    if isinstance(vocab_note, VocabNote) and ui_utils.is_displaytype_displaying_answer(_type_of_display):
        html = render_kanji_names(vocab_note, html)

    return html


def render_kanji_names(vocab_note: VocabNote, html: str) -> str:
    def prepare_kanji_meaning(kanji: KanjiNote) -> str:
        meaning = kanji.get_answer()
        meaning = meaning.strip().replace(",", "/").replace(" ", "")
        return meaning

    kanji_list = [char for char in ex_str.extract_characters(vocab_note.get_question()) if kana_utils.is_kanji(char)]

    kanji_names:list[str] = list()
    for kanji_character in kanji_list:
        kanji_note = app.col().kanji.with_kanji(kanji_character)
        if kanji_note:
            kanji_names.append(prepare_kanji_meaning(kanji_note))
        else:
            kanji_names.append("MISSING KANJI")

    html = html.replace("##KANJI_NAMES##", " # ".join(kanji_names))

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_compound_list)
