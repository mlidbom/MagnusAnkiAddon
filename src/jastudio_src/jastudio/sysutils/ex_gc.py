from __future__ import annotations

import gc

from jastudio.ankiutils import app
from JAStudio.Core import MyLog
from jastudio.sysutils import app_thread_pool


def collect_on_ui_thread_and_display_message(message: str = "Garbage collecting") -> None:
    def collect_with_progress() -> None:
        MyLog.Info("collect_with_progress")
        import gc
        app.get_ui_utils().tool_tip(message, 6000)
        gc.collect()

    app_thread_pool.run_on_ui_thread_synchronously(collect_with_progress)

def collect_on_ui_thread_synchronously() -> None:
    app_thread_pool.run_on_ui_thread_synchronously(gc.collect)
