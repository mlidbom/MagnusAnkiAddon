using System;
using System.Collections.Generic;
using Avalonia;
using Avalonia.Controls;
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
            ItemsSource = new List<MenuItem> { clipboardItem, selectionItem }
        };
        
        // Close the host window when the context menu closes
        contextMenu.Closed += (s, e) => _hostWindow?.Close();
        
        return contextMenu;
    }

    public void ShowAt(int x, int y)
    {
        // Create a transparent window at the specified location
        _hostWindow = new Window
        {
            Width = 1,
            Height = 1,
            Position = new PixelPoint(x, y),
            WindowStartupLocation = WindowStartupLocation.Manual,
            ShowInTaskbar = false,
            SystemDecorations = SystemDecorations.None,
            Background = Avalonia.Media.Brushes.Transparent,
            TransparencyLevelHint = new[] { WindowTransparencyLevel.Transparent },
            Topmost = true
        };

        var contextMenu = CreateContextMenu();
        
        _hostWindow.Opened += (s, e) =>
        {
            // Open the context menu on this window
            contextMenu.Open(_hostWindow);
        };
        
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
        // For now, just show a message - this is where you'd implement actual functionality
        System.Diagnostics.Debug.WriteLine($"Clipboard item clicked: {_clipboardContent}");
    }

    private void OnSelectionItemClick(object? sender, RoutedEventArgs e)
    {
        // For now, just show a message - this is where you'd implement actual functionality
        System.Diagnostics.Debug.WriteLine($"Selection item clicked: {_selectionContent}");
    }
}
