import re

from anki.cards import Card
from aqt import gui_hooks

from sysutils import my_clipboard
from sysutils.utils import UIUtils


def copy_previewer_sort_field_to_windows_clipboard(html:str, card: Card, type_of_display:str) -> str:
    if type_of_display == 'previewAnswer':
        if not UIUtils.is_edit_current_active():
            copy_card_sort_field_to_clipboard(card)
    return html


class CopyCardData:
    note_id = 0


def copy_card_sort_field_to_clipboard(card):
    note = card.note()
    if note.id == CopyCardData.note_id:
        return
    else:
        CopyCardData.note_id = note.id
    model = note.model()
    sort_field = model['sortf']
    sort_value = note.fields[sort_field]
    clean_string = re.sub('<.*?>', '', sort_value)
    clean_string = re.sub('\[.*?\]', '', clean_string) # noqa
    my_clipboard.set_text(clean_string)


def init():
    gui_hooks.reviewer_did_show_answer.append(copy_card_sort_field_to_clipboard)
    gui_hooks.card_will_show.append(copy_previewer_sort_field_to_windows_clipboard)
