from __future__ import annotations

from jaslib.task_runners.task_progress_runner import TaskRunner
from jaspythonutils.sysutils.typed import non_optional

from jastudio.qt_utils.qt_task_progress_runner import QtTaskProgressRunner

# The JAStudioAppRoot composition root instance, set during init().
# Other modules import this to access C# UI services.
app_root = None


def init() -> None:

    from jastudio.ui import garbage_collection_fixes, hooks, menus, timing_hacks, tools_menu, web
    _init_dot_net_app()
    hooks.init()
    timing_hacks.init()
    tools_menu.init()
    web.init()
    menus.init()
    garbage_collection_fixes.init()
    TaskRunner.set_ui_task_runner_factory(QtTaskProgressRunner)

def _init_dot_net_app() -> None:
    global app_root
    from JAStudio.UI import JAStudioAppRoot
    from System import Action

    from jastudio.configuration.configuration_value import get_config_json, write_config_dict_json
    from jastudio.ankiutils import app as ja_app

    config_json = get_config_json()
    config_update_callback = Action[str](write_config_dict_json)  # pyright: ignore [reportCallIssue]
    app_root = JAStudioAppRoot.Initialize(config_json, config_update_callback)

    # Load collection data once Anki's profile/collection is ready
    ja_app._init_hooks.add(lambda: non_optional(app_root).LoadCollection())
