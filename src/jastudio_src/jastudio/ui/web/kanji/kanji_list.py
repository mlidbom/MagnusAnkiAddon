from __future__ import annotations

import re
from typing import TYPE_CHECKING

from aqt import gui_hooks
from jaslib import app
from jaslib.note.kanjinote import KanjiNote
from jaslib.sysutils import ex_str, kana_utils
from jaslib.viewmodels.kanji_list.sentence_kanji_viewmodel import KanjiViewModel

from jastudio.ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer

if TYPE_CHECKING:
    from jaslib.note.jpnote import JPNote


def render_list(note:JPNote, kanjis:list[KanjiNote], kanji_readings:list[str]) -> str:
    if not kanjis:
        return ""

    # noinspection DuplicatedCode
    def highlight_inherited_reading(text: str) -> str:
        for reading in kanji_readings:
            text = re.sub(rf"\b{re.escape(kana_utils.katakana_to_hiragana(reading))}\b", f"<inherited-reading>{kana_utils.katakana_to_hiragana(reading)}</inherited-reading>", text)
            text = re.sub(rf"\b{re.escape(kana_utils.hiragana_to_katakana(reading))}\b", f"<inherited-reading>{kana_utils.hiragana_to_katakana(reading)}</inherited-reading>", text)

        return text

    def prefer__studying_kanji(kan: KanjiNote) -> int:
        return 0 if kan.is_studying() else 1

    kanjis = [kan for kan in kanjis if kan != note]
    kanjis = sorted(kanjis, key=lambda kan: prefer__studying_kanji(kan))

    viewmodels = [KanjiViewModel(kanji) for kanji in kanjis]

    return f"""
    <div id="kanji_list" class="page_section">
        <div class="page_section_title">kanji</div>
    {ex_str.newline.join(f'''
        <div class="kanji_item {" ".join(kanji.kanji.get_meta_tags())}">
            <div class="kanji_main">
                <span class="kanji_kanji clipboard">{kanji.question()}</span>
                <span class="kanji_readings">{highlight_inherited_reading(kanji.readings())}</span>
                <span class="kanji_answer">{kanji.answer()}</span>
            </div>
            <div class="kanji_mnemonic">{kanji.mnemonic()}</div>
        </div>
    ''' for kanji in viewmodels)}
    </div>
            """


def kanji_kanji_list(kanji:KanjiNote) -> str:
    kanjis = app.col().kanji.with_radical(kanji.get_question())
    kanji_readings = kanji.get_readings_clean()

    return render_list(kanji, kanjis, kanji_readings)


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(KanjiNote, {"##KANJI_LIST##": kanji_kanji_list}).render)