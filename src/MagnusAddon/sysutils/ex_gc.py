from __future__ import annotations

import mylog
from ankiutils import app
from sysutils import app_thread_pool


def collect_on_on_ui_thread_if_collection_during_batches_enabled() -> bool:
    def collect_with_progress() -> None:
        mylog.info("collect_with_progress")
        import gc
        app.get_ui_utils().tool_tip("Garbage collecting", 6000)
        gc.collect()

    if app.config().enable_garbage_collection_during_batches.get_value():
        app_thread_pool.run_on_ui_thread_synchronously(collect_with_progress)
        return True

    return False
