"""
PyQt adapter for UI-agnostic menu specifications.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from aqt.qt import QAction, QKeySequence, QMenu
from jaspythonutils.sysutils.typed import non_optional

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

        if spec.IsSubmenu:
            qt_sub_menu = non_optional(target_qt_menu.addMenu(spec.Name))
            add_to_qt_menu(qt_sub_menu, spec.Children)
        elif spec.IsSeparator:
            target_qt_menu.addSeparator()
        elif spec.IsCommand:
            action = QAction(spec.Name, target_qt_menu)
            action.setEnabled(spec.IsEnabled)

            if spec.KeyboardShortcut:
                action.setShortcut(QKeySequence(spec.KeyboardShortcut))

            if spec.IsCommand:
                action.triggered.connect(lambda checked, a=spec.Action: a.Invoke())  # pyright: ignore [reportUnknownMemberType, reportUnknownLambdaType]
            target_qt_menu.addAction(action)  # pyright: ignore [reportUnknownMemberType]
        else:
            raise Exception(f"Unknown menu spec type: {spec}")
