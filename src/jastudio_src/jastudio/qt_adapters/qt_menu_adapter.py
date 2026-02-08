"""
PyQt adapter for UI-agnostic menu specifications.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from aqt.qt import QAction, QKeySequence, QMenu
from jaspythonutils.sysutils.typed import non_optional

if TYPE_CHECKING:
    from collections.abc import Iterable

    from JAStudio.UI.Menus.UIAgnosticMenuStructure import SpecMenuItem, SpecMenuItemKind
else:
    from JAStudio.UI.Menus.UIAgnosticMenuStructure import SpecMenuItemKind

def add_to_qt_menu(target_qt_menu: QMenu, specs: Iterable[SpecMenuItem]) -> None:
    """
    Add C# menu specs to a parent QMenu. This is the single integration point for adding C#-defined menus to PyQt.
    """
    for spec in specs:
        if not spec.IsVisible:
            continue

        name_with_accelerator = _add_acceleratator_key_to_name(spec.Name, spec.KeyboardShortcut)

        if spec.Kind == SpecMenuItemKind.Submenu:
            qt_sub_menu = non_optional(target_qt_menu.addMenu(name_with_accelerator))
            qt_sub_menu.setEnabled(spec.IsEnabled)
            add_to_qt_menu(qt_sub_menu, spec.Children)
        elif spec.Kind == SpecMenuItemKind.Separator:
            target_qt_menu.addSeparator()
        elif spec.Kind == SpecMenuItemKind.Command:
            action = QAction(name_with_accelerator, target_qt_menu)
            action.setEnabled(spec.IsEnabled)

            if spec.KeyboardShortcut:
                action.setShortcut(QKeySequence(spec.KeyboardShortcut))

            action.triggered.connect(lambda urdu, a=spec.Action: a.Invoke())  # pyright: ignore [reportUnknownMemberType, reportUnknownLambdaType]
            target_qt_menu.addAction(action)  # pyright: ignore [reportUnknownMemberType]
        else:
            raise Exception(f"Unknown menu spec type: {spec.Name}")

def _add_acceleratator_key_to_name(name: str, accelerator: str) -> str:
    name = name.replace("_","&")
    if not accelerator: return name
    return f"&{accelerator.replace} {name}"
