using System;
using System.Collections.Generic;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.Primitives;
using Avalonia.Interactivity;

namespace JAStudio.UI.Views;

public partial class ContextMenuPopup : UserControl
{
    private readonly string _clipboardContent;
    private readonly string _selectionContent;
    private Window? _hostWindow;

    public ContextMenuPopup(string clipboardContent, string selectionContent)
    {
        _clipboardContent = clipboardContent;
        _selectionContent = selectionContent;
        
        InitializeComponent();
    }

    public ContextMenu CreateContextMenu()
    {
        var clipboardItem = new MenuItem
        {
            Header = string.IsNullOrEmpty(_clipboardContent) 
                ? "Clipboard: (empty)" 
                : $"Clipboard: {TruncateText(_clipboardContent, 30)}"
        };
        clipboardItem.Click += OnClipboardItemClick;
        
        var selectionItem = new MenuItem
        {
            Header = string.IsNullOrEmpty(_selectionContent) 
                ? "Selection: (empty)" 
                : $"Selection: {TruncateText(_selectionContent, 30)}"
        };
        selectionItem.Click += OnSelectionItemClick;
        
        var contextMenu = new ContextMenu
        {
            ItemsSource = new List<MenuItem> { clipboardItem, selectionItem },
            Placement = PlacementMode.Pointer
        };
        
        // Close the host window when the context menu closes
        contextMenu.Closed += (s, e) => _hostWindow?.Close();
        
        return contextMenu;
    }

    public void ShowAt(int x, int y)
    {
        JALogger.Log($"ShowAt called with: ({x}, {y})");
        
        // Create sub-menu items
        var clipboardItem = new MenuItem
        {
            Header = string.IsNullOrEmpty(_clipboardContent) 
                ? "Clipboard: (empty)" 
                : $"Clipboard: {TruncateText(_clipboardContent, 30)}"
        };
        clipboardItem.Click += OnClipboardItemClick;
        
        var selectionItem = new MenuItem
        {
            Header = string.IsNullOrEmpty(_selectionContent) 
                ? "Selection: (empty)" 
                : $"Selection: {TruncateText(_selectionContent, 30)}"
        };
        selectionItem.Click += OnSelectionItemClick;
        
        // Create a top-level menu item that contains our items as a submenu
        var topMenuItem = new MenuItem
        {
            Header = "▼", // Just a visual indicator, or empty
            ItemsSource = new List<MenuItem> { clipboardItem, selectionItem }
        };
        
        // Create the main menu
        var menu = new Menu
        {
            ItemsSource = new List<MenuItem> { topMenuItem }
        };
        
        // Create window with the Menu as content
        _hostWindow = new Window
        {
            Content = menu,
            WindowStartupLocation = WindowStartupLocation.Manual,
            CanResize = false,
            ShowInTaskbar = false,
            SystemDecorations = SystemDecorations.None,
            Background = Avalonia.Media.Brushes.White,
            SizeToContent = SizeToContent.WidthAndHeight,
            Topmost = true
        };
        
        _hostWindow.Opened += (s, e) =>
        {
            _hostWindow.Position = new PixelPoint(x, y);
            JALogger.Log($"Window opened at ({x}, {y}), size: {_hostWindow.Bounds}");
            
            // Open the submenu immediately
            topMenuItem.IsSubMenuOpen = true;
            JALogger.Log("Submenu opened");
        };
        
        // Close when the submenu closes or window loses focus
        topMenuItem.PropertyChanged += (s, e) =>
        {
            if (e.Property.Name == nameof(MenuItem.IsSubMenuOpen) && !topMenuItem.IsSubMenuOpen)
            {
                _hostWindow?.Close();
            }
        };
        
        _hostWindow.Deactivated += (s, e) => _hostWindow.Close();
        
        _hostWindow.Show();
    }

    private static string TruncateText(string text, int maxLength)
    {
        if (text.Length <= maxLength)
            return text;
        return text.Substring(0, maxLength) + "...";
    }

    private void OnClipboardItemClick(object? sender, RoutedEventArgs e)
    {
        JALogger.Log($"Clipboard item clicked: {_clipboardContent}");
    }

    private void OnSelectionItemClick(object? sender, RoutedEventArgs e)
    {
        JALogger.Log($"Selection item clicked: {_selectionContent}");
    }
}

