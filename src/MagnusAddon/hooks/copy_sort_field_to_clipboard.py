import pyperclip
from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app
from ankiutils.app import ui_utils
from note.jpnote import JPNote
from sysutils.collections.recent_items import RecentItems
from sysutils import ex_str

recent_previewer_cards = RecentItems[int](2)

def copy_card_sort_field_to_clipboard(note: JPNote) -> None:
    clean_string = ex_str.strip_html_and_bracket_markup_and_noise_characters(note.get_question())
    pyperclip.copy(clean_string)

recent_review_answers = RecentItems[int](1)
def on_reviewer_show_answer(card: Card) -> None:
    note = app.col().note_by_id(card.nid)
    if note:
        if ui_utils().is_edit_current_open() or recent_review_answers.is_recent(note.get_id()):
            return

        copy_card_sort_field_to_clipboard(note)

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(on_reviewer_show_answer)