"""
Backend for JAStudio.Core.Anki.AnkiFacade - handles Qt thread marshaling.

All functions in this module ensure they execute on the Qt main thread,
making them safe to call from any .NET thread (including the Avalonia UI thread).
"""
from __future__ import annotations

from anki.cards import CardId
from anki.notes import NoteId
from jaspythonutils.sysutils.typed import non_optional
from jastudio.sysutils.app_thread_pool import run_on_ui_thread_fire_and_forget, run_on_ui_thread_synchronously
from typed_linq_collections.q_iterable import query

# ── Browser ──

def browser_execute_lookup(query: str) -> None:
    """Execute an Anki browser search query."""
    def do_it() -> None:
        from jastudio.ankiutils import search_executor
        search_executor.do_lookup(query)
    run_on_ui_thread_fire_and_forget(do_it)


def browser_execute_lookup_and_show_previewer(query: str) -> None:
    """Execute an Anki browser search query and show the previewer."""
    def do_it() -> None:
        from jastudio.ankiutils import search_executor
        search_executor.do_lookup_and_show_previewer(query)
    run_on_ui_thread_fire_and_forget(do_it)


def browser_prioritize_cards(card_ids: list[int]) -> None:
    """Prioritize selected cards (sets card.due based on note type priority)."""
    def do_it() -> None:
        from jastudio.note import queue_manager
        queue_manager.prioritize_selected_cards(query(card_ids).select(NoteId).to_list())
    run_on_ui_thread_fire_and_forget(do_it)


def browser_spread_cards_over_days(card_ids: list[int], start_day: int, days_apart: int) -> None:
    """Spread selected cards over days (distributes due dates across time range)."""
    def do_it() -> None:
        from jastudio.ui.menus.browser import main as browser_main
        browser_main.spread_due_dates(query(card_ids).select(NoteId).to_list(), start_day, days_apart)
    run_on_ui_thread_fire_and_forget(do_it)


# ── UIUtils ──

def ui_show_tooltip(message: str, period_ms: int = 3000) -> None:
    """Show a tooltip message in Anki."""
    def do_it() -> None:
        from aqt.utils import tooltip
        tooltip(message, period_ms)
    run_on_ui_thread_fire_and_forget(do_it)


def ui_refresh() -> None:
    """Refresh the currently displayed views in Anki."""
    def do_it() -> None:
        from jastudio.ankiutils import app
        app.get_ui_utils().refresh()
    run_on_ui_thread_fire_and_forget(do_it)


# ── Batches ──

def batches_convert_immersion_kit_sentences() -> None:
    """Convert Immersion Kit sentences to the standard sentence note type."""
    def do_it() -> None:
        from jastudio.batches import local_note_updater
        local_note_updater.convert_immersion_kit_sentences()
    run_on_ui_thread_fire_and_forget(do_it)


# ── NoteEx ──

def note_suspend_all_cards(note_id: int) -> None:
    """Suspend all cards for the given note ID."""
    def do_it() -> None:
        from jastudio.anki_extentions.note_ex import NoteEx
        NoteEx.from_id(note_id).suspend_all_cards()
    run_on_ui_thread_fire_and_forget(do_it)


def note_unsuspend_all_cards(note_id: int) -> None:
    """Unsuspend all cards for the given note ID."""
    def do_it() -> None:
        from jastudio.anki_extentions.note_ex import NoteEx
        NoteEx.from_id(note_id).un_suspend_all_cards()
    run_on_ui_thread_fire_and_forget(do_it)


# ── Col ──

def col_db_file_path() -> str:
    """Get the path to the Anki collection database file."""
    def do_it() -> str:
        from aqt import mw
        return non_optional(mw.col).path
    return run_on_ui_thread_synchronously(do_it)


# ── Misc ──

def get_note_id_from_card_id(card_id: int) -> int:
    """Get note ID from card ID."""
    def do_it() -> int:
        from jastudio.ankiutils import app
        return int(app.anki_collection().get_card(CardId(card_id)).nid)
    return run_on_ui_thread_synchronously(do_it)
