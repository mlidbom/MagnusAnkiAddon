from anki.cards import Card
from anki.notes import Note
from aqt import gui_hooks

from ankiutils import search_utils
from note.mynote import MyNote
from sysutils import my_clipboard
from sysutils.collections.recent_items import RecentItems
from sysutils.utils import StringUtils
from sysutils.ui_utils import UIUtils

recent_note_ids = RecentItems[int](2)

def copy_previewer_sort_field_to_windows_clipboard(html:str, card: Card, type_of_display:str) -> str:
    if (type_of_display == 'previewAnswer'
            and not UIUtils.is_edit_current_open()
            and not recent_note_ids.is_recent(card.note().id)):
        copy_card_sort_field_to_clipboard(card.note())
    return html

def copy_card_sort_field_to_clipboard(note: Note) -> None:
    model = note.model()
    sort_field = model['sortf']
    sort_value = note.fields[sort_field]
    clean_string = StringUtils.strip_markup_and_noise_characters(sort_value)
    my_clipboard.set_text(clean_string)


def show_dependencies_in_browser(note: Note) -> None:
    search_utils.lookup_dependencies(MyNote.note_from_note(note))

def on_reviewer_show_answer(card: Card) -> None:
    note = card.note()
    if UIUtils.is_edit_current_open() or recent_note_ids.is_recent(note.id):
        return

    show_dependencies_in_browser(note)
    copy_card_sort_field_to_clipboard(note)

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(on_reviewer_show_answer)
    gui_hooks.card_will_show.append(copy_previewer_sort_field_to_windows_clipboard)
