using System;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace JAStudio.UI.Views;

public partial class ContextMenuPopup : Window
{
    private readonly string _clipboardContent;
    private readonly string _selectionContent;
    private PixelPoint? _desiredPosition;

    public ContextMenuPopup(string clipboardContent, string selectionContent)
    {
        _clipboardContent = clipboardContent;
        _selectionContent = selectionContent;
        
        InitializeComponent();
        
        // Set the menu item headers
        ClipboardMenuItem.Header = string.IsNullOrEmpty(clipboardContent) 
            ? "Clipboard: (empty)" 
            : $"Clipboard: {TruncateText(clipboardContent, 30)}";
            
        SelectionMenuItem.Header = string.IsNullOrEmpty(selectionContent) 
            ? "Selection: (empty)" 
            : $"Selection: {TruncateText(selectionContent, 30)}";
    }

    public void SetDesiredPosition(PixelPoint position)
    {
        _desiredPosition = position;
        // Apply position immediately if already opened
        if (IsVisible)
        {
            Position = position;
        }
    }

    protected override void OnOpened(EventArgs e)
    {
        base.OnOpened(e);
        
        // Force the position after the window opens
        if (_desiredPosition.HasValue)
        {
            Position = _desiredPosition.Value;
        }
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
        Close();
    }

    private void OnSelectionItemClick(object? sender, RoutedEventArgs e)
    {
        // For now, just show a message - this is where you'd implement actual functionality
        System.Diagnostics.Debug.WriteLine($"Selection item clicked: {_selectionContent}");
        Close();
    }
}
