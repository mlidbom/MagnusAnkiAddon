from typing import cast

from anki.cards import Card
from anki.models import NotetypeDict
from anki.notes import Note
from aqt import gui_hooks

from hooks.timing_hacks import ugly_timing_hacks
from sysutils import my_clipboard
from sysutils.collections.recent_items import RecentItems
from sysutils.stringutils import StringUtils
from ankiutils.ui_utils import UIUtils

recent_previewer_cards = RecentItems[int](2)
def copy_previewer_sort_field_to_windows_clipboard(html:str, card: Card, type_of_display:str) -> str:
    if ((type_of_display == 'previewAnswer'
            and not UIUtils.is_edit_current_open()
            and not recent_previewer_cards.is_recent(card.note().id))
            and not ugly_timing_hacks.reviewer_just_showed_answer()):
        copy_card_sort_field_to_clipboard(card.note())
    return html

def copy_card_sort_field_to_clipboard(note: Note) -> None:
    model = cast(NotetypeDict, note.note_type())
    sort_field = model['sortf']
    sort_value = note.fields[sort_field]
    clean_string = StringUtils.strip_html_and_bracket_markup_and_noise_characters(sort_value)
    my_clipboard.set_text(clean_string)

recent_review_answers = RecentItems[int](1)
def on_reviewer_show_answer(card: Card) -> None:
    note = card.note()
    if UIUtils.is_edit_current_open() or recent_review_answers.is_recent(note.id):
        return

    copy_card_sort_field_to_clipboard(note)

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(on_reviewer_show_answer)
    gui_hooks.card_will_show.append(copy_previewer_sort_field_to_windows_clipboard)
