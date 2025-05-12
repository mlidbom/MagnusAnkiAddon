from __future__ import annotations

from aqt import gui_hooks
from hooks.note_content_building.content_renderer import PrerenderingAnswerContentRenderer
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_str
from viewmodels.kanji_list import sentence_kanji_list_viewmodel


def render_kanji_list_from_kanji(kanjis:list[str]) -> str:
    if not kanjis:
        return ""

    viewmodel = sentence_kanji_list_viewmodel.create(kanjis)

    return f"""
<div id="kanji_list" class="page_section">
    <div class="page_section_title">kanji</div>
{ex_str.newline.join(f'''
    <div class="kanji_item {" ".join(kanji.kanji.get_meta_tags())}">
        <div class="kanji_main">
            <span class="kanji_kanji clipboard">{kanji.question()}</span>
            <span class="kanji_readings">{kanji.readings()}</span>
            <span class="kanji_answer">{kanji.answer()}</span>        
        </div>
        <div class="kanji_mnemonic">{kanji.mnemonic()}</div>
    </div>
''' for kanji in viewmodel.kanji_list)}
</div>
        """

def render_vocab_kanji_list(vocab: VocabNote) -> str:
    return render_kanji_list_from_kanji(vocab.extract_main_form_kanji())

def render_sentence_kanji_list(sentence: SentenceNote) -> str:
    return render_kanji_list_from_kanji(sentence.extract_kanji())


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {"##KANJI_LIST##": render_vocab_kanji_list}).render)
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, {"##KANJI_LIST##": render_sentence_kanji_list}).render)