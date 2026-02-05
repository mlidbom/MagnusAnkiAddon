using System;
using System.Collections.Generic;

namespace JAStudio.UI.Menus.UIAgnosticMenuStructure;

/// <summary>
/// UI-agnostic menu item specification. Represents either a leaf command, a submenu container, or a separator.
/// This specification is independent of any UI framework (Avalonia, WPF, Qt, etc.) and can be passed to
/// framework-specific adapters that recursively build the actual UI menu structure.
/// Can also be passed to Python via pythonnet for building menus in PyQt.
/// </summary>
public class MenuItem
{
    /// <summary>
    /// Display name of the menu item (e.g., "Open in Browser", "Lookup").
    /// For separators, this should be null or empty.
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Keyboard accelerator character for Alt+Key navigation (e.g., 'K' for Alt+K).
    /// Used by ShortcutFinger to generate underlined accelerator text in Name.
    /// </summary>
    public char? AcceleratorKey { get; set; }

    /// <summary>
    /// Action to execute when this menu item is clicked.
    /// Null for submenus and separators.
    /// </summary>
    public Action? Action { get; set; }

    /// <summary>
    /// Child menu items for submenus.
    /// Null or empty for leaf commands and separators.
    /// </summary>
    public IReadOnlyList<MenuItem>? Children { get; set; }

    /// <summary>
    /// If true, this item is a visual separator (horizontal line) between menu groups.
    /// When true, Name and Action should be null/empty.
    /// </summary>
    public bool IsSeparator { get; set; }

    /// <summary>
    /// Keyboard shortcut display text (e.g., "Ctrl+O", "Ctrl+Shift+S").
    /// This is for display only - actual keyboard handling happens elsewhere.
    /// </summary>
    public string? KeyboardShortcut { get; set; }

    /// <summary>
    /// Whether the menu item is enabled (clickable).
    /// Disabled items appear grayed out but remain visible.
    /// </summary>
    public bool IsEnabled { get; set; } = true;

    /// <summary>
    /// Whether the menu item is visible in the menu.
    /// Use this for conditional menu items that should be completely hidden.
    /// </summary>
    public bool IsVisible { get; set; } = true;

    /// <summary>
    /// Create a separator menu item (horizontal divider line).
    /// </summary>
    public static MenuItem Separator() => new MenuItem { IsSeparator = true };

    /// <summary>
    /// Create a leaf command menu item.
    /// </summary>
    public static MenuItem Command(string name, Action action, char? acceleratorKey = null, string? shortcut = null, bool enabled = true)
    {
        return new MenuItem
        {
            Name = name,
            Action = action,
            AcceleratorKey = acceleratorKey,
            KeyboardShortcut = shortcut,
            IsEnabled = enabled
        };
    }

    /// <summary>
    /// Create a submenu container.
    /// </summary>
    public static MenuItem Submenu(string name, IReadOnlyList<MenuItem> children, char? acceleratorKey = null)
    {
        return new MenuItem
        {
            Name = name,
            Children = children,
            AcceleratorKey = acceleratorKey
        };
    }

    /// <summary>
    /// Is this a leaf command (has an action to execute)?
    /// </summary>
    public bool IsCommand => Action != null;

    /// <summary>
    /// Is this a submenu (has children)?
    /// </summary>
    public bool IsSubmenu => Children != null && Children.Count > 0;
}
