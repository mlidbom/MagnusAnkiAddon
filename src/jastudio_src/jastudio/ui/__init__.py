from __future__ import annotations

from jaspythonutils.sysutils.typed import non_optional

from jastudio.task_runners.task_progress_runner import TaskRunner

# The JAStudioAppRoot composition root instance, set during init().
# Other modules import this to access C# UI services.
dotnet_ui_root = None


def init() -> None:
    _init_dot_net_app()
    from jastudio.ui import garbage_collection_fixes, hooks, menus, timing_hacks, tools_menu, web
    hooks.init()
    timing_hacks.init()
    tools_menu.init()
    web.init()
    menus.init()
    garbage_collection_fixes.init()
    from jastudio.qt_utils.qt_task_progress_runner import QtTaskProgressRunner
    TaskRunner.set_ui_task_runner_factory(QtTaskProgressRunner)

def _init_dot_net_app() -> None:
    global dotnet_ui_root
    from JAStudio.UI import JAStudioAppRoot
    from System import Action

    from jastudio.configuration.configuration_value import get_config_json, write_config_dict_json

    config_json = get_config_json()
    config_update_callback = Action[str](write_config_dict_json)  # pyright: ignore [reportCallIssue]
    dotnet_ui_root = JAStudioAppRoot.Initialize(config_json, config_update_callback)
