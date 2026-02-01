from __future__ import annotations

from jastudio.qt_utils.qt_task_progress_runner import QtTaskProgressRunner
from jastudio.qt_utils.task_progress_runner import TaskRunner


def init() -> None:
    from ui import garbage_collection_fixes, hooks, menus, timing_hacks, tools_menu, web
    hooks.init()
    timing_hacks.init()
    tools_menu.init()
    web.init()
    menus.init()
    garbage_collection_fixes.init()

    TaskRunner.set_ui_task_runner_factory(QtTaskProgressRunner)
