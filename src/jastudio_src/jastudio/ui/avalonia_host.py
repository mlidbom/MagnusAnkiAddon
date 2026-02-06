"""
Avalonia UI integration for JAStudio.

This module provides Python wrappers for the C# Avalonia UI dialogs.
Call initialize() once at addon startup, then use the show_* functions.
"""
from __future__ import annotations

from JAStudio.UI import DialogHost


def show_about_dialog() -> None: DialogHost.ShowAboutDialog()
def show_options_dialog() -> None: DialogHost.ShowOptionsDialog()
def toggle_note_search_dialog() -> None: DialogHost.ToggleNoteSearchDialog()
