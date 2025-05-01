from aqt import gui_hooks

from hooks.note_content_building.content_renderer import PrerenderingAnswerContentRenderer
from note.kanjinote import KanjiNote

def render_mnemonic(note: KanjiNote) -> str:
    return note.get_active_mnemonic()

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(KanjiNote, {"##MNEMONIC##": render_mnemonic}).render)