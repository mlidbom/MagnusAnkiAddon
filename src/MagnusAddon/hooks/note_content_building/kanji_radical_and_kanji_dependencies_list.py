import re

from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app, ui_utils
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

        dependencies = app.col().kanji.display_dependencies_of(note)

        if dependencies:
            list_html = f"""
    <div id="dependencies_list" class="page_section">
        <div class="page_section_title">radicals</div>
    {ex_str.newline.join(f'''
        <div class="dependency">
            <div class="dependency_heading">
                {f'<div class="dependency_character clipboard">{dependency.character}</div>'
                if dependency.character
                else f'<div class="dependency_icon">{dependency.icon_substitute_for_character}</div>'}
                
            
                <div class="dependency_name clipboard">{dependency.name}</div>
                <div class="dependency_readings">{highlight_primary_reading_sources(", ".join(dependency.readings))}</div>
            </div>
            <div class="dependency_mnemonic">{dependency.mnemonic}</div>
        </div>
    ''' for dependency in dependencies)}
    </div>
            """

            html = html.replace("##DEPENDENCIES_LIST##", list_html)
        else:
            html = html.replace("##DEPENDENCIES_LIST##", "")

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_dependencies_list)