using System.Collections.Generic;
using Avalonia.Controls;
using JAStudio.UI;

namespace JAStudio.UI.Examples;

/// <summary>
/// Examples showing how to create menus and position them using PopupMenuHost.
/// Build your menu structure using standard Avalonia MenuItem classes,
/// then use PopupMenuHost.ShowAt() to display it at any screen coordinates.
/// </summary>
public static class MenuExamples
{
    /// <summary>
    /// Example: Simple flat menu
    /// </summary>
    public static void ShowSimpleMenu(int x, int y)
    {
        var item1 = new MenuItem { Header = "Action 1" };
        item1.Click += (s, e) => JALogger.Log("Action 1 clicked");
        
        var item2 = new MenuItem { Header = "Action 2" };
        item2.Click += (s, e) => JALogger.Log("Action 2 clicked");
        
        var menuItems = new List<MenuItem> { item1, item2 };
        PopupMenuHost.ShowAt(menuItems, x, y);
    }
    
    /// <summary>
    /// Example: Menu with nested submenus (arbitrary depth)
    /// </summary>
    public static void ShowNestedMenu(int x, int y)
    {
        // Create submenu items
        var subItem1 = new MenuItem { Header = "Sub Action 1" };
        subItem1.Click += (s, e) => JALogger.Log("Sub Action 1 clicked");
        
        var subItem2 = new MenuItem { Header = "Sub Action 2" };
        subItem2.Click += (s, e) => JALogger.Log("Sub Action 2 clicked");
        
        // Create a nested submenu (level 3)
        var deepItem1 = new MenuItem { Header = "Deep Action 1" };
        deepItem1.Click += (s, e) => JALogger.Log("Deep Action 1 clicked");
        
        var deepItem2 = new MenuItem { Header = "Deep Action 2" };
        deepItem2.Click += (s, e) => JALogger.Log("Deep Action 2 clicked");
        
        var nestedSubmenu = new MenuItem
        {
            Header = "More Options...",
            ItemsSource = new List<MenuItem> { deepItem1, deepItem2 }
        };
        
        // Create top-level submenu
        var submenu = new MenuItem
        {
            Header = "Tools",
            ItemsSource = new List<MenuItem> { subItem1, subItem2, nestedSubmenu }
        };
        
        // Top-level items
        var item1 = new MenuItem { Header = "Open" };
        item1.Click += (s, e) => JALogger.Log("Open clicked");
        
        var separator = new Separator();
        
        // Build the complete menu
        var menuItems = new List<MenuItem>
        {
            item1,
            submenu,
            new MenuItem { Header = "-" }, // Separator can also be added this way
            new MenuItem { Header = "Exit" }
        };
        
        PopupMenuHost.ShowAt(menuItems, x, y);
    }
    
    /// <summary>
    /// Example: Dynamically built menu (e.g., from a list of items)
    /// </summary>
    public static void ShowDynamicMenu(string[] items, int x, int y)
    {
        var menuItems = new List<MenuItem>();
        
        foreach (var item in items)
        {
            var menuItem = new MenuItem { Header = item };
            var capturedItem = item; // Capture for closure
            menuItem.Click += (s, e) => JALogger.Log($"Clicked: {capturedItem}");
            menuItems.Add(menuItem);
        }
        
        PopupMenuHost.ShowAt(menuItems, x, y);
    }
}
