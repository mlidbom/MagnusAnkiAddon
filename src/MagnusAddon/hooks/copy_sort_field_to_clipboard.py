import pyperclip  # type: ignore
from typing import cast

from anki.cards import Card
from anki.models import NotetypeDict
from anki.notes import Note
from aqt import gui_hooks

from ankiutils import app
from ankiutils.app import ui_utils
from sysutils.collections.recent_items import RecentItems
from sysutils import app_thread_pool, ex_str
from sysutils.timeutil import StopWatch

def copy_card_sort_field_to_clipboard(note: Note) -> None:
    with StopWatch.log_warning_if_slower_than(0.01):
        if app.config().yomitan_integration_copy_answer_to_clipboard.get_value():
            model = cast(NotetypeDict, note.note_type())
            sort_field = model['sortf']
            sort_value = note.fields[sort_field]
            clean_string = ex_str.strip_html_and_bracket_markup_and_noise_characters(sort_value)
            app_thread_pool.pool.submit(lambda: pyperclip.copy(clean_string))

recent_review_answers = RecentItems[int](1)
def on_reviewer_show_answer(card: Card) -> None:
    note = card.note()
    if ui_utils().is_edit_current_open() or recent_review_answers.is_recent(note.id):
        return

    copy_card_sort_field_to_clipboard(note)

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(on_reviewer_show_answer)