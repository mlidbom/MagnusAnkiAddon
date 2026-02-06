"""
PyQt adapter for UI-agnostic menu specifications.

This is the Python/PyQt equivalent of AvaloniaMenuAdapter.cs.
Converts JAStudio.UI.Menus.UIAgnosticMenuStructure.MenuItem specs to native PyQt QMenus.

All menu structure and business logic lives in C# - this is just a thin adapter.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from aqt.qt import QAction, QKeySequence, QMenu

if TYPE_CHECKING:
    from collections.abc import Iterable

    from JAStudio.UI.Menus.UIAgnosticMenuStructure import SpecMenuItem


def to_qmenu(spec: SpecMenuItem, parent: QMenu | None = None) -> QMenu:
    if spec.IsSeparator:
        raise ValueError("to_qmenu should not be called on separators - parent handles them")

    # Create root menu or use parent
    menu = QMenu(spec.Name) if parent is None else parent

    if spec.IsSubmenu:
        for child_spec in spec.Children:
            if not child_spec.IsVisible:
                continue

            if child_spec.IsSeparator:
                menu.addSeparator()
            elif child_spec.IsSubmenu:
                submenu = menu.addMenu(child_spec.Name)
                to_qmenu(child_spec, submenu)
            else:
                action = QAction(child_spec.Name, menu)
                action.setEnabled(child_spec.IsEnabled)

                if child_spec.KeyboardShortcut:
                    action.setShortcut(QKeySequence(child_spec.KeyboardShortcut))

                if child_spec.IsCommand:
                    action.triggered.connect(lambda checked, a=child_spec.Action: a.Invoke())  # pyright: ignore [reportUnknownMemberType, reportUnknownLambdaType]
                menu.addAction(action)  # pyright: ignore [reportUnknownMemberType]

    return menu


def to_qmenu_list(specs: Iterable[SpecMenuItem]) -> list[QMenu]:
    result: list[QMenu] = []
    for spec in specs:
        if not spec.IsVisible:
            continue
        if not spec.IsSeparator:
            result.append(to_qmenu(spec))
    return result