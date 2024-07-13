from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from sysutils import ex_str

def render_dependencies_list(html: str, card: Card, _type_of_display: str) -> str:
    note = JPNote.note_from_card(card)

    if isinstance(note, KanjiNote):
        dependencies = app.col().kanji.display_dependencies_of(note)

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
            <div class="dependency_readings">{", ".join(dependency.readings)}</div>
        </div>
        <div class="dependency_mnemonic">{dependency.mnemonic}</div>
    </div>
''' for dependency in dependencies)}
</div>
        """

        html = html.replace("##DEPENDENCIES_LIST##", list_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_dependencies_list)