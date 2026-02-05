"""
PyQt adapter for UI-agnostic menu specifications.

This is the Python/PyQt equivalent of AvaloniaMenuAdapter.cs.
Converts JAStudio.UI.Menus.UIAgnosticMenuStructure.MenuItem specs to native PyQt QMenus.

All menu structure and business logic lives in C# - this is just a thin adapter.
"""

from aqt.qt import QMenu, QAction, QKeySequence
from JAStudio.UI.Menus.UIAgnosticMenuStructure import MenuItem as SpecMenuItem


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
    if spec.Children is not None and len(spec.Children) > 0:
        for child_spec in spec.Children:
            if not child_spec.IsVisible:
                continue  # Skip invisible items
            
            if child_spec.IsSeparator:
                menu.addSeparator()
            elif child_spec.IsSubmenu:
                # Create submenu recursively
                submenu = menu.addMenu(child_spec.Name)
                to_qmenu(child_spec, submenu)
            else:
                # Leaf command - create action
                action = QAction(child_spec.Name, menu)
                action.setEnabled(child_spec.IsEnabled)
                
                # Add keyboard shortcut if specified
                if child_spec.KeyboardShortcut:
                    try:
                        action.setShortcut(QKeySequence(child_spec.KeyboardShortcut))
                    except:
                        # If parsing fails, just skip the shortcut
                        # Actual keyboard handling is done elsewhere via Anki's shortcut system
                        pass
                
                # Wire up the action
                if child_spec.Action is not None:
                    # Connect to C# Action - pythonnet handles the marshaling
                    action.triggered.connect(lambda checked, a=child_spec.Action: _invoke_action(a))
                
                menu.addAction(action)
    
    return menu


def to_qmenu_list(specs: list[SpecMenuItem]) -> list[QMenu]:
    """
    Convert a list of MenuItem specs to PyQt QMenus.
    Useful for building entire menu bars at once.
    
    Args:
        specs: List of MenuItem specifications from C#
        
    Returns:
        List of QMenus built from the specifications
    """
    result = []
    for spec in specs:
        if not spec.IsVisible:
            continue
        if not spec.IsSeparator:  # Skip separators at the top level
            result.append(to_qmenu(spec))
    return result


def _invoke_action(action):
    """
    Invoke a C# Action with proper error handling.
    Follows JAStudio exception handling policy - log and re-raise.
    """
    try:
        action()
    except Exception as e:
        # Log the error
        from jastudio.utils.logging import log_error
        log_error(f"Menu action failed: {e}")
        # Re-raise per project exception handling policy
        raise
