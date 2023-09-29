from anki.cards import Card
from anki.notes import Note
from aqt import gui_hooks

from ankiutils import search_utils
from note.jpnote import JPNote
from sysutils.collections.recent_items import RecentItems
from sysutils.ui_utils import UIUtils


def show_dependencies_in_browser(note: Note) -> None:
    search_utils.lookup_dependencies(JPNote.note_from_note(note))

recent_review_answers = RecentItems[int](1)
def on_reviewer_show_answer(card: Card) -> None:
    note = card.note()
    if UIUtils.is_edit_current_open() or recent_review_answers.is_recent(note.id):
        return

    show_dependencies_in_browser(note)

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(on_reviewer_show_answer)
