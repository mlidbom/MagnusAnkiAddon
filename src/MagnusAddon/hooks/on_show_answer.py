from anki.cards import Card
from aqt import gui_hooks

from sysutils import my_clipboard
from sysutils.collections.recent_items import RecentItems
from sysutils.utils import StringUtils
from sysutils.ui_utils import UIUtils

recent_note_ids = RecentItems[int](2)

def copy_previewer_sort_field_to_windows_clipboard(html:str, card: Card, type_of_display:str) -> str:
    if type_of_display == 'previewAnswer':
        copy_card_sort_field_to_clipboard(card)
    return html

def copy_card_sort_field_to_clipboard(card: Card) -> None:
    note = card.note()
    if UIUtils.is_edit_current_open() or recent_note_ids.is_recent(note.id): return

    model = note.model()
    sort_field = model['sortf']
    sort_value = note.fields[sort_field]
    clean_string = StringUtils.strip_markup_and_noise_characters(sort_value)
    my_clipboard.set_text(clean_string)


def show_dependencies_in_browser(card: Card) -> None:
    pass

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(copy_card_sort_field_to_clipboard)
    gui_hooks.reviewer_did_show_answer.append(show_dependencies_in_browser)
    gui_hooks.card_will_show.append(copy_previewer_sort_field_to_windows_clipboard)
