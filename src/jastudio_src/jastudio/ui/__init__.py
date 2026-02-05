from __future__ import annotations

from jaslib.task_runners.task_progress_runner import TaskRunner

from jastudio.qt_utils.qt_task_progress_runner import QtTaskProgressRunner


def init() -> None:
    from jastudio.ui import avalonia_host, garbage_collection_fixes, hooks, menus, timing_hacks, tools_menu, web
    hooks.init()
    timing_hacks.init()
    tools_menu.init()
    web.init()
    menus.init()
    garbage_collection_fixes.init()
    avalonia_host.initialize()

    TaskRunner.set_ui_task_runner_factory(QtTaskProgressRunner)
