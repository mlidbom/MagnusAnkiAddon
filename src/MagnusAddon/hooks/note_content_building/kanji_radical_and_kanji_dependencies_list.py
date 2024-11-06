import re

from anki.cards import Card
from aqt import gui_hooks

from ankiutils import ui_utils
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from sysutils import ex_str, kana_utils

def render_dependencies_list(html: str, card: Card, _type_of_display: str) -> str:
    if not ui_utils.is_displaytype_displaying_answer(_type_of_display):
        return html

    note = JPNote.note_from_card(card)

    if isinstance(note, KanjiNote):
        readings = note.get_readings_clean()

        def highlight_primary_reading_sources(text: str) -> str:
            for reading in readings:
                text = re.sub(rf'\b{re.escape(kana_utils.to_hiragana(reading))}\b', f"<primary-reading-source>{kana_utils.to_hiragana(reading)}</primary-reading-source>", text)
                text = re.sub(rf'\b{re.escape(kana_utils.to_katakana(reading))}\b', f"<primary-reading-source>{kana_utils.to_katakana(reading)}</primary-reading-source>", text)

            return text

        dependencies = note.get_radicals_notes()

        def format_readings(_kanji: KanjiNote) -> str:
            separator = """<span class="readingsSeparator">|</span>"""

            readings_on = ", ".join([kana_utils.to_katakana(reading) for reading in _kanji.get_reading_on_list_html()])
            readings_kun = ", ".join(_kanji.get_reading_kun_list_html())

            return f"""{readings_on} {separator} {readings_kun}"""

        if dependencies:
            list_html = f"""
    <div id="dependencies_list" class="page_section">
        <div class="page_section_title">radicals</div>
    {ex_str.newline.join(f'''
        <div class="dependency {" ".join(kanji.get_meta_tags())}">
            <div class="dependency_heading">
                <div class="dependency_character clipboard">{kanji.get_question()}</div>                           
                <div class="dependency_name clipboard">{kanji.get_answer()}</div>
                <div class="dependency_readings">{highlight_primary_reading_sources(format_readings(kanji))}</div>
            </div>
            <div class="dependency_mnemonic">{kanji.get_user_mnemonic()}</div>
        </div>
    ''' for kanji in dependencies)}
    </div>
            """

            html = html.replace("##DEPENDENCIES_LIST##", list_html)
        else:
            html = html.replace("##DEPENDENCIES_LIST##", "")

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_dependencies_list)