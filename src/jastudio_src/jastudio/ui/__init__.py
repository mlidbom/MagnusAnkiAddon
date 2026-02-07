from __future__ import annotations

from jaslib.task_runners.task_progress_runner import TaskRunner

from jastudio.qt_utils.qt_task_progress_runner import QtTaskProgressRunner

# The JAStudioAppRoot composition root instance, set during init().
# Other modules import this to access C# UI services.
app_root = None


def init() -> None:
    global app_root
    from jastudio.ui import garbage_collection_fixes, hooks, menus, timing_hacks, tools_menu, web
    hooks.init()
    timing_hacks.init()
    tools_menu.init()
    web.init()
    menus.init()
    garbage_collection_fixes.init()

    from JAStudio.UI import JAStudioAppRoot
    app_root = JAStudioAppRoot.Initialize()

    TaskRunner.set_ui_task_runner_factory(QtTaskProgressRunner)
