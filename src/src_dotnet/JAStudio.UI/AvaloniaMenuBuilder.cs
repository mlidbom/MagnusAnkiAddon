using System;
using System.Collections.Generic;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.Primitives;
using Avalonia.Interactivity;

namespace JAStudio.UI;

/// <summary>
/// Builder for creating Avalonia popup menus that can be shown at any screen position.
/// Hides the "ugly hack" of using a transparent window with a hidden top-level menu item.
/// </summary>
public class AvaloniaMenuBuilder
{
    private readonly List<MenuItemConfig> _items = new();

    /// <summary>
    /// Configuration for a single menu item.
    /// </summary>
    public class MenuItemConfig
    {
        public required string Label { get; init; }
        public Action? OnClick { get; init; }
    }

    /// <summary>
    /// Add a menu item with a label and click handler.
    /// </summary>
    public AvaloniaMenuBuilder AddItem(string label, Action onClick)
    {
        _items.Add(new MenuItemConfig { Label = label, OnClick = onClick });
        return this;
    }

    /// <summary>
    /// Show the menu at the specified screen coordinates.
    /// </summary>
    /// <param name="x">X coordinate in physical (device) pixels</param>
    /// <param name="y">Y coordinate in physical (device) pixels</param>
    public void ShowAt(int x, int y)
    {
        var menuItems = new List<MenuItem>();
        
        foreach (var config in _items)
        {
            var menuItem = new MenuItem
            {
                Header = config.Label
            };
            
            if (config.OnClick != null)
            {
                menuItem.Click += (s, e) =>
                {
                    try
                    {
                        config.OnClick();
                    }
                    catch (Exception ex)
                    {
                        JALogger.Log($"Menu item click error: {ex}");
                    }
                };
            }
            
            menuItems.Add(menuItem);
        }

        ShowMenuAtPosition(menuItems, x, y);
    }

    /// <summary>
    /// Internal implementation: Show menu at position using the transparent window hack.
    /// </summary>
    private static void ShowMenuAtPosition(List<MenuItem> menuItems, int x, int y)
    {
        // Create a top-level menu item that contains our items as a submenu
        // We make this invisible to minimize visual presence
        var topMenuItem = new MenuItem
        {
            Header = "", // Empty header
            ItemsSource = menuItems,
            Height = 0,
            MinHeight = 0,
            Padding = new Thickness(0),
            Margin = new Thickness(0)
        };
        
        // Create the main menu (required to host the MenuItem)
        var menu = new Menu
        {
            ItemsSource = new List<MenuItem> { topMenuItem },
            Height = 0,
            Padding = new Thickness(0),
            Margin = new Thickness(0)
        };
        
        // Create window with the Menu as content
        var hostWindow = new Window
        {
            Content = menu,
            WindowStartupLocation = WindowStartupLocation.Manual,
            CanResize = false,
            ShowInTaskbar = false,
            SystemDecorations = SystemDecorations.None,
            Background = Avalonia.Media.Brushes.Transparent,
            SizeToContent = SizeToContent.Manual,
            Width = 1,
            Height = 1,
            Topmost = true
        };
        
        hostWindow.Opened += (s, e) =>
        {
            // Get the actual height of the menu bar and adjust for DPI
            var menuHeight = (int)(hostWindow.Bounds.Height * 1.25); // Convert logical to physical pixels at 125% DPI
            
            // Offset the window upward by the menu height so the submenu appears at the correct position
            var adjustedY = y - menuHeight;
            
            hostWindow.Position = new PixelPoint(x, adjustedY);
            JALogger.Log($"Menu window opened at ({x}, {adjustedY}), original y: {y}");
            
            // Open the submenu immediately
            topMenuItem.IsSubMenuOpen = true;
        };
        
        // Close when the submenu closes or window loses focus
        topMenuItem.PropertyChanged += (s, e) =>
        {
            if (e.Property.Name == nameof(MenuItem.IsSubMenuOpen) && !topMenuItem.IsSubMenuOpen)
            {
                hostWindow.Close();
            }
        };
        
        hostWindow.Deactivated += (s, e) => hostWindow.Close();
        
        hostWindow.Show();
    }
}
