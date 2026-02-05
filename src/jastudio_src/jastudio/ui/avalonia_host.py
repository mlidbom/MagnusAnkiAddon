"""
Avalonia UI integration for JAStudio.

This module provides Python wrappers for the C# Avalonia UI dialogs.
Call initialize() once at addon startup, then use the show_* functions.
"""
from __future__ import annotations

from jaslib import mylog

_initialized = False


def initialize() -> None:
    """Initialize the Avalonia UI subsystem. Call once at addon startup."""
    global _initialized
    if _initialized:
        return

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]

        DialogHost.Initialize()  # pyright: ignore[reportUnknownMemberType]
        _initialized = True
        mylog.info("Avalonia UI initialized")
    except Exception as e:
        mylog.error(f"Failed to initialize Avalonia UI: {e}")
        raise


def shutdown() -> None:
    """Shutdown the Avalonia UI subsystem. Call at addon unload."""
    global _initialized
    if not _initialized:
        return

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]

        DialogHost.Shutdown()  # pyright: ignore[reportUnknownMemberType]
        _initialized = False
        mylog.info("Avalonia UI shutdown")
    except Exception as e:
        mylog.error(f"Failed to shutdown Avalonia UI: {e}")


def show_about_dialog() -> None:
    """Show the Avalonia About dialog."""
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]

        DialogHost.ShowAboutDialog()  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        mylog.error(f"Failed to show AboutDialog: {e}")
        raise


def show_context_menu_popup(clipboard_content: str, selection_content: str, x: int, y: int) -> None:
    """
    Show the Avalonia context menu popup at the specified screen coordinates.

    Args:
        clipboard_content: Content from clipboard
        selection_content: Currently selected text
        x: X coordinate (screen coordinates)
        y: Y coordinate (screen coordinates)
    """
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]

        DialogHost.ShowContextMenuPopup(clipboard_content, selection_content, x, y)  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        mylog.error(f"Failed to show context menu popup: {e}")
        raise
