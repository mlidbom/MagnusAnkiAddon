from aqt import gui_hooks

from hooks.note_content_building.content_renderer import PrerenderingAnswerSingleTagContentRenderer
from note.kanjinote import KanjiNote
from sysutils import kana_utils
from sysutils.timeutil import StopWatch

def render_katakana_onyomi(kanji_note: KanjiNote) -> str:
    with StopWatch.log_warning_if_slower_than("render_katakana_onyomi", 0.001):
        on_readings_list = [kana_utils.to_katakana(x) for x in kanji_note.get_reading_on_list_html()]
        on_readings = ", ".join(f"""<span class="clipboard">{reading}</span>""" for reading in on_readings_list)
        kun_readings = ", ".join(f"""<span class="clipboard">{reading}</span>""" for reading in kanji_note.get_reading_kun_list_html())
        nan_readings = ", ".join(f"""<span class="clipboard">{reading}</span>""" for reading in kanji_note.get_reading_nan_list_html())

        readings_html = f"""
         <span class="reading">{on_readings}</span> <span class="readingsSeparator">|</span>
         <span class="reading">{kun_readings}</span> <span class="readingsSeparator">|</span>
         <span class="reading">{nan_readings}</span>
    """

        return readings_html


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerSingleTagContentRenderer(KanjiNote, "##KANJI_READINGS##", render_katakana_onyomi).render)
