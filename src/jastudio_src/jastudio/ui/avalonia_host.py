"""
Avalonia UI integration for JAStudio.

This module provides Python wrappers for the C# Avalonia UI dialogs.
Call initialize() once at addon startup, then use the show_* functions.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pyperclip
from jaslib import mylog

if TYPE_CHECKING:
    from collections.abc import Callable

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


def show_options_dialog() -> None:
    """Show the Avalonia Options dialog for Japanese configuration settings."""
    mylog.info("show_options_dialog() called")
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        mylog.info("Importing DialogHost...")
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]

        mylog.info("Calling DialogHost.ShowOptionsDialog()...")
        DialogHost.ShowOptionsDialog()  # pyright: ignore[reportUnknownMemberType]
        mylog.info("OptionsDialog shown successfully")
    except Exception as e:
        mylog.error(f"Failed to show OptionsDialog: {e}")
        import traceback
        mylog.error(traceback.format_exc())
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


def show_test_main_menu(x: int, y: int) -> None:
    """
    Show the test main menu (Japanese Avalonia) at the specified screen coordinates.

    Args:
        x: X coordinate (screen coordinates, physical pixels)
        y: Y coordinate (screen coordinates, physical pixels)
    """
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]

        DialogHost.ShowTestMainMenu(x, y)  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        mylog.error(f"Failed to show test main menu: {e}")
        raise


def show_japanese_main_menu(refresh_callback: Callable[[], None], x: int, y: int) -> None:
    """
    Show the Japanese main menu at the specified screen coordinates.

    Args:
        refresh_callback: Callback to invoke Anki UI refresh
        x: X coordinate (screen coordinates, physical pixels)
        y: Y coordinate (screen coordinates, physical pixels)
    """
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
        from System import Action  # pyright: ignore[reportMissingImports]

        from jastudio.ankiutils import search_executor

        # Wrap Python callbacks in .NET delegates
        refresh_action = Action(refresh_callback)  # pyright: ignore[reportCallIssue]

        def execute_lookup(query: str) -> None:
            search_executor.do_lookup(query)

        lookup_action = Action[str](execute_lookup)  # pyright: ignore[reportCallIssue]

        # Get clipboard text for searches (no selection context in main menu)
        search_text = pyperclip.paste().strip()

        DialogHost.ShowJapaneseMainMenu(refresh_action, lookup_action, search_text, x, y)  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        mylog.error(f"Failed to show Japanese main menu: {e}")
        raise


def show_vocab_context_menu(refresh_callback: Callable[[], None], selection: str, clipboard: str, x: int, y: int) -> None:
    """Show context menu for a vocab note."""
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
        from System import Action  # pyright: ignore[reportMissingImports]

        from jastudio.ankiutils import search_executor

        refresh_action = Action(refresh_callback)  # pyright: ignore[reportCallIssue]

        def execute_lookup(query: str) -> None:
            search_executor.do_lookup(query)

        lookup_action = Action[str](execute_lookup)  # pyright: ignore[reportCallIssue]

        DialogHost.ShowVocabContextMenu(refresh_action, lookup_action, selection, clipboard, x, y)  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        mylog.error(f"Failed to show vocab context menu: {e}")
        raise


def show_kanji_context_menu(refresh_callback: Callable[[], None], selection: str, clipboard: str, x: int, y: int) -> None:
    """Show context menu for a kanji note."""
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
        from System import Action  # pyright: ignore[reportMissingImports]

        from jastudio.ankiutils import search_executor

        refresh_action = Action(refresh_callback)  # pyright: ignore[reportCallIssue]

        def execute_lookup(query: str) -> None:
            search_executor.do_lookup(query)

        lookup_action = Action[str](execute_lookup)  # pyright: ignore[reportCallIssue]

        DialogHost.ShowKanjiContextMenu(refresh_action, lookup_action, selection, clipboard, x, y)  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        mylog.error(f"Failed to show kanji context menu: {e}")
        raise


def show_sentence_context_menu(refresh_callback: Callable[[], None], selection: str, clipboard: str, x: int, y: int) -> None:
    """Show context menu for a sentence note."""
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
        from System import Action  # pyright: ignore[reportMissingImports]

        from jastudio.ankiutils import search_executor

        refresh_action = Action(refresh_callback)  # pyright: ignore[reportCallIssue]

        def execute_lookup(query: str) -> None:
            search_executor.do_lookup(query)

        lookup_action = Action[str](execute_lookup)  # pyright: ignore[reportCallIssue]

        DialogHost.ShowSentenceContextMenu(refresh_action, lookup_action, selection, clipboard, x, y)  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        mylog.error(f"Failed to show sentence context menu: {e}")
        raise


def show_generic_context_menu(refresh_callback: Callable[[], None], selection: str, clipboard: str, x: int, y: int) -> None:
    """Show context menu when no note is available."""
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]
        from System import Action  # pyright: ignore[reportMissingImports]

        from jastudio.ankiutils import search_executor

        refresh_action = Action(refresh_callback)  # pyright: ignore[reportCallIssue]

        def execute_lookup(query: str) -> None:
            search_executor.do_lookup(query)

        lookup_action = Action[str](execute_lookup)  # pyright: ignore[reportCallIssue]

        DialogHost.ShowGenericContextMenu(refresh_action, lookup_action, selection, clipboard, x, y)  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        mylog.error(f"Failed to show generic context menu: {e}")
        raise


def show_test_context_menu(selection: str, clipboard: str, x: int, y: int) -> None:
    """
    Show the test context menu at the specified screen coordinates.

    Args:
        selection: Currently selected text
        clipboard: Clipboard content
        x: X coordinate (screen coordinates, physical pixels)
        y: Y coordinate (screen coordinates, physical pixels)
    """
    if not _initialized:
        mylog.warning("Avalonia UI not initialized, initializing now...")
        initialize()

    try:
        from JAStudio.UI import DialogHost  # pyright: ignore[reportMissingImports, reportUnknownVariableType]

        DialogHost.ShowTestContextMenu(selection, clipboard, x, y)  # pyright: ignore[reportUnknownMemberType]
    except Exception as e:
        mylog.error(f"Failed to show test context menu: {e}")
        raise
