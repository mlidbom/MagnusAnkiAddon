"""Helper for adding hover-triggered Avalonia menu items to PyQt menus."""
from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QMenu


def add_hover_avalonia_menu(
    menu: QMenu,
    action_label: str,
    show_avalonia_menu: Callable[[int, int], None],
) -> None:
    """
    Add a menu action that shows an Avalonia menu on hover.
    
    This handles all the boilerplate:
    - Creating the Qt menu action
    - Tracking hover state to prevent duplicate shows
    - Converting Qt coordinates to Avalonia physical pixels
    - Auto-resetting state after a delay
    
    Args:
        menu: The Qt menu to add the action to
        action_label: The text label for the menu action
        show_avalonia_menu: Callback that shows the Avalonia menu.
                           Will be called with (physical_x, physical_y) coordinates.
    """
    from PyQt6.QtCore import QTimer

    avalonia_action = menu.addAction(action_label)  # pyright: ignore[reportUnknownMemberType]

    # Track if we've already shown the popup for this hover
    shown = False
    reset_timer: QTimer | None = None

    def on_reset() -> None:
        """Reset the shown flag."""
        nonlocal shown
        shown = False

    def on_hover() -> None:
        """Called when the action is hovered."""
        nonlocal shown, reset_timer

        if shown:
            return
        shown = True

        # Reset the flag after a short delay (allows re-triggering on next menu open)
        if reset_timer:
            reset_timer.stop()

        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: on_reset())  # pyright: ignore[reportUnknownMemberType]
        timer.start(500)  # Reset after 500ms
        reset_timer = timer

        try:
            from PyQt6.QtWidgets import QApplication

            # Get the action's geometry within the menu
            action_rect = menu.actionGeometry(avalonia_action)

            # Map the action's top-left corner to global screen coordinates
            action_global_pos = menu.mapToGlobal(action_rect.topLeft())

            # Get DPI scale factor to convert logical pixels to physical pixels
            screen = QApplication.screenAt(action_global_pos)
            dpi_scale = screen.devicePixelRatio() if screen else 1.0

            # Convert to physical pixels for Avalonia
            physical_x = int(action_global_pos.x() * dpi_scale)
            physical_y = int(action_global_pos.y() * dpi_scale)

            # Show the Avalonia menu
            show_avalonia_menu(physical_x, physical_y)
        except Exception as e:
            from jaslib import mylog

            mylog.error(f"Failed to show Avalonia menu: {e}")

    # Connect the hover event
    avalonia_action.hovered.connect(on_hover)  # pyright: ignore[reportUnknownMemberType, reportOptionalMemberAccess]
