from anki.cards import Card
from aqt import gui_hooks

from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from sysutils import kana_utils



def render_katakana_onyomi(html: str, card: Card, _type_of_display: str) -> str:
    kanji_note = JPNote.note_from_card(card)

    if isinstance(kanji_note, KanjiNote):
        html = html.replace("##KATAKANA_ONYOMI##", kana_utils.to_katakana(kanji_note.get_reading_on()))

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_katakana_onyomi)
