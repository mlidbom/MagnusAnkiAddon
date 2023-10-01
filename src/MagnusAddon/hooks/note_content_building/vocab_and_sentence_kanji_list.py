from anki.cards import Card
from aqt import gui_hooks

from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils.stringutils import StringUtils
from viewmodels import sentence_kanji_list_viewmodel


def render_kanji_list(html:str, card: Card, _type_of_display:str) -> str:
    note = JPNote.note_from_card(card)
    question:str = ""

    if isinstance(note, VocabNote):
        question = note.get_question()
    elif isinstance(note, SentenceNote):
        question = note.get_active_question()

    if question:
        viewmodel = sentence_kanji_list_viewmodel.create(note)

        list_html = f"""
<div id="kanji_list">
{StringUtils.newline().join(f'''
    <div class="kanji_item">
        <span class="kanji_kanji clipboard">{kanji.question()}</span>
        <span class="kanji_answer">{kanji.answer()}</span>
        <span class="kanji_readings">{kanji.readings()}</span>
    </div>
    <div class="kanji_mnemonic">{kanji.mnemonic()}</div>
''' for kanji in viewmodel.kanji_list)}
</div>
        """

        html = html.replace("##KANJI_LIST##", list_html)

    return html


def init() -> None:
    gui_hooks.card_will_show.append(render_kanji_list)