from anki.cards import Card
from aqt import gui_hooks

from ankiutils import search_utils
from note.mynote import MyNote
from note.sentencenote import SentenceNote
from note.kanjinote import KanjiNote
from note.vocabnote import VocabNote
from sysutils import kana_utils
from sysutils.utils import StringUtils, ListUtils
from note.jp_collection import JPCollection


def render_kanji_list(html:str, card: Card, _type_of_display:str) -> str:
    note = MyNote.note_from_card(card)
    question:str = ""

    if isinstance(note, VocabNote):
        question = note.get_question()
    elif isinstance(note, SentenceNote):
        question = note.get_active_question()

    if question:
        question = StringUtils.remove_duplicates_characters(question)
        kanji_list:list[KanjiNote] = ListUtils.flatten_list([JPCollection.search_kanji_notes(search_utils.fetch_kanji_by_kanji([c])) for c in question])

        list_html = f"""
<div id="kanji_list">
{StringUtils.newline().join(f'''
    <div class="kanji_item">
        <span class="kanji_kanji clipboard">{kanji.get_question()}</span>
        <span class="kanji_answer">{kanji.get_active_answer()}</span>
        <span class="kanji_readings">{kanji.get_reading_kun()}, {kana_utils.to_katakana(kanji.get_reading_on())}</span>
    </div>
    <div class="kanji_mnemonic">{kanji.get_mnemonics_override() if kanji.get_mnemonics_override() not in {"-", ""} else ""}</div>
''' for kanji in kanji_list)}
</div>
        """

        html = html.replace("##KANJI_LIST##", list_html)

    return html


def init() -> None:
    gui_hooks.card_will_show.append(render_kanji_list)