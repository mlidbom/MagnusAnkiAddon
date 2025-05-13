from __future__ import annotations

from sysutils import app_thread_pool


def collect_on_on_ui_thread() -> None:
    import gc
    app_thread_pool.run_on_ui_thread_synchronously(lambda: gc.collect())
