from __future__ import annotations

import gc

import mylog

from jastudio.ankiutils import app
from jastudio.sysutils import app_thread_pool


def collect_on_on_ui_thread_if_collection_during_batches_enabled(display: bool = True) -> bool:
    if app.config().enable_garbage_collection_during_batches.get_value():
        if display:
            collect_on_ui_thread_and_display_message()
        else:
            app_thread_pool.run_on_ui_thread_synchronously(lambda: gc.collect())
        return True

    return False

def collect_on_ui_thread_and_display_message(message: str = "Garbage collecting") -> None:
    def collect_with_progress() -> None:
        mylog.info("collect_with_progress")
        import gc
        app.get_ui_utils().tool_tip(message, 6000)
        gc.collect()

    app_thread_pool.run_on_ui_thread_synchronously(collect_with_progress)

def collect_on_ui_thread_synchronously() -> None:
    app_thread_pool.run_on_ui_thread_synchronously(gc.collect)
