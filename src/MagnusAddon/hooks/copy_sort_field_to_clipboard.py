import pyperclip  # type: ignore
from typing import cast

from anki.cards import Card
from anki.models import NotetypeDict
from anki.notes import Note
from aqt import gui_hooks

from ankiutils.app import ui_utils
from sysutils.collections.recent_items import RecentItems
from sysutils import ex_str
from concurrent.futures import ThreadPoolExecutor

recent_previewer_cards = RecentItems[int](2)

executor = ThreadPoolExecutor()

def copy_card_sort_field_to_clipboard(note: Note) -> None:
    model = cast(NotetypeDict, note.note_type())
    sort_field = model['sortf']
    sort_value = note.fields[sort_field]
    clean_string = ex_str.strip_html_and_bracket_markup_and_noise_characters(sort_value)
    executor.submit(lambda: pyperclip.copy(clean_string))

recent_review_answers = RecentItems[int](1)
def on_reviewer_show_answer(card: Card) -> None:
    note = card.note()
    if ui_utils().is_edit_current_open() or recent_review_answers.is_recent(note.id):
        return

    copy_card_sort_field_to_clipboard(note)

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(on_reviewer_show_answer)