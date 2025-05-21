from __future__ import annotations

from ui import clear_studying_cache_on_card_suspend_unsuspend, copy_sort_field_to_clipboard, custom_auto_advance_timings, custom_short_term_scheduling, custom_shortcuts, custom_timebox_lengths, editor_buttons, history_navigator, menus, no_accidental_double_click, timebox_end_sound, timing_hacks, tools_menu, web


def init() -> None:
    clear_studying_cache_on_card_suspend_unsuspend.init()
    copy_sort_field_to_clipboard.init()
    custom_auto_advance_timings.init()
    custom_short_term_scheduling.init()
    custom_shortcuts.init()
    custom_timebox_lengths.init()
    editor_buttons.init()
    history_navigator.init()
    no_accidental_double_click.init()
    timebox_end_sound.init()
    timing_hacks.init()
    tools_menu.init()
    web.init()
    menus.init()
