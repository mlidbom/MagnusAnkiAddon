from __future__ import annotations

from typing import TYPE_CHECKING

from jaslib.viewmodels.kanji_list import sentence_kanji_list_viewmodel
from jaspythonutils.sysutils import ex_str

if TYPE_CHECKING:
    from jaslib.note.vocabulary.vocabnote import VocabNote


def render_kanji_list_from_kanji(kanjis: list[str]) -> str:
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
            <span class="kanji_answer">{kanji.answer()}</span>
            <span class="kanji_readings">{kanji.readings()}</span>
        </div>
        <div class="kanji_mnemonic">{kanji.mnemonic()}</div>
    </div>
''' for kanji in viewmodel.kanji_list)}
</div>
        """

def render_vocab_kanji_list(vocab: VocabNote) -> str:
    return render_kanji_list_from_kanji(vocab.kanji.extract_main_form_kanji())