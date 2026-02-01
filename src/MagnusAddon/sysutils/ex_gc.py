from __future__ import annotations

from ankiutils import app


def collect_on_on_ui_thread_if_collection_during_batches_enabled() -> bool:
    if app.config().enable_garbage_collection_during_batches.get_value():
        collect_on_ui_thread_and_display_message()
        return True

    return False

def collect_on_ui_thread_and_display_message() -> None:
    import gc
    gc.collect()

def collect_on_ui_thread_synchronously() -> None:
    collect_on_ui_thread_and_display_message()
