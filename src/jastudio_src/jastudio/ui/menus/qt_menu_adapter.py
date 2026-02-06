"""
PyQt adapter for UI-agnostic menu specifications.

This is the Python/PyQt equivalent of AvaloniaMenuAdapter.cs.
Converts JAStudio.UI.Menus.UIAgnosticMenuStructure.MenuItem specs to native PyQt QMenus.

All menu structure and business logic lives in C# - this is just a thin adapter.
"""

from aqt.qt import QMenu, QAction, QKeySequence
from JAStudio.UI.Menus.UIAgnosticMenuStructure import MenuItem as SpecMenuItem  # pyright: ignore[reportMissingImports]

from collections.abc import Iterable


def to_qmenu(spec: SpecMenuItem, parent: QMenu | None = None) -> QMenu:
    """
    Convert a UI-agnostic MenuItem spec to a PyQt QMenu.
    Recursively builds submenus.
    
    Args:
        spec: The MenuItem specification from C#
        parent: Optional parent QMenu for building submenus
        
    Returns:
        QMenu built from the specification
    """
    if spec.IsSeparator:
        # Separators should be handled by the parent menu
        raise ValueError("to_qmenu should not be called on separators - parent handles them")
    
    # Create root menu or use parent
    if parent is None:
        menu = QMenu(spec.Name)
    else:
        menu = parent
    
    # If this is a submenu, build its children
    if spec.Children is not None and spec.Children.Count > 0:  # pyright: ignore[reportUnknownMemberType, reportUnnecessaryComparison]
        for child_spec in spec.Children:  # pyright: ignore[reportUnknownVariableType]
            if not child_spec.IsVisible:  # pyright: ignore[reportUnknownMemberType]
                continue  # Skip invisible items
            
            if child_spec.IsSeparator:  # pyright: ignore[reportUnknownMemberType]
                menu.addSeparator()
            elif child_spec.IsSubmenu:  # pyright: ignore[reportUnknownMemberType]
                # Create submenu recursively
                submenu = menu.addMenu(child_spec.Name)  # pyright: ignore[reportUnknownMemberType]
                to_qmenu(child_spec, submenu)  # pyright: ignore[reportUnknownArgumentType]
            else:
                # Leaf command - create action
                action = QAction(child_spec.Name, menu)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
                action.setEnabled(child_spec.IsEnabled)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
                
                # Add keyboard shortcut if specified
                if child_spec.KeyboardShortcut:  # pyright: ignore[reportUnknownMemberType]
                    try:
                        action.setShortcut(QKeySequence(child_spec.KeyboardShortcut))  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
                    except:  # noqa: E722
                        # If parsing fails, just skip the shortcut
                        # Actual keyboard handling is done elsewhere via Anki's shortcut system
                        pass
                
                # Wire up the action
                if child_spec.Action is not None:  # pyright: ignore[reportUnknownMemberType, reportUnnecessaryComparison]
                    # Connect to C# Action - pythonnet handles the marshaling
                    action.triggered.connect(lambda checked, a=child_spec.Action: _invoke_action(a))  # pyright: ignore[reportUnknownMemberType, reportUnknownLambdaType]
                
                menu.addAction(action)  # pyright: ignore[reportUnknownMemberType]
    
    return menu


def to_qmenu_list(specs: Iterable[SpecMenuItem]) -> list[QMenu]:
    """
    Convert a list of MenuItem specs to PyQt QMenus.
    Useful for building entire menu bars at once.
    
    Args:
        specs: List of MenuItem specifications from C#
        
    Returns:
        List of QMenus built from the specifications
    """
    result: list[QMenu] = []
    for spec in specs:
        if not spec.IsVisible:  # pyright: ignore[reportUnknownMemberType]
            continue
        if not spec.IsSeparator:  # pyright: ignore[reportUnknownMemberType] # Skip separators at the top level
            result.append(to_qmenu(spec))
    return result


def _invoke_action(action):  # type: ignore[no-untyped-def]  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    """
    Invoke a C# Action with proper error handling.
    Follows JAStudio exception handling policy - log and re-raise.
    """
    try:
        action()  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        from jaslib import mylog
        mylog.error(f"Menu action failed: {e}")
        # Re-raise per project exception handling policy
        raise
