"""
PyQt adapter for UI-agnostic menu specifications.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from aqt.qt import QAction, QKeySequence, QMenu
from jaspythonutils.sysutils.typed import non_optional

from jastudio import mylog

if TYPE_CHECKING:
    from collections.abc import Iterable

    from JAStudio.UI.Menus.UIAgnosticMenuStructure import SpecMenuItem

def add_to_qt_menu(target_qt_menu: QMenu, specs: Iterable[SpecMenuItem]) -> None:
    """
    Add C# menu specs to a parent QMenu. This is the single integration point for adding C#-defined menus to PyQt.
    """
    for spec in specs:
        if not spec.IsVisible:
            continue

        name_with_accelerator = _add_acceleratator_key_to_name(spec.Name, spec.KeyboardShortcut)

        if spec.IsSubmenu:
            qt_sub_menu = non_optional(target_qt_menu.addMenu(name_with_accelerator))
            add_to_qt_menu(qt_sub_menu, spec.Children)
        elif spec.IsSeparator:
            target_qt_menu.addSeparator()
        elif spec.IsCommand:
            action = QAction(name_with_accelerator, target_qt_menu)
            action.setEnabled(spec.IsEnabled)

            if spec.KeyboardShortcut:
                action.setShortcut(QKeySequence(spec.KeyboardShortcut))

            action.triggered.connect(lambda urdu, a=spec.Action: a.Invoke())  # pyright: ignore [reportUnknownMemberType, reportUnknownLambdaType]
            target_qt_menu.addAction(action)  # pyright: ignore [reportUnknownMemberType]
        else:
            mylog.error(f"Unknown menu spec type: {spec.Name}")
            #target_qt_menu.addAction(f"Unknown menu-spec named: {spec.Name}")  # pyright: ignore [reportUnknownMemberType]
            #raise Exception(f"Unknown menu spec type: {spec.Name}")

def _add_acceleratator_key_to_name(name: str, accelerator: str) -> str:
    if accelerator == "": return name
    return f"&{accelerator} {name}"
