using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Media;

namespace JAStudio.UI.Views;

public partial class ContextMenuPopup : Window
{
    private readonly string _clipboardContent;
    private readonly string _selectionContent;

    public ContextMenuPopup(string clipboardContent, string selectionContent)
    {
        _clipboardContent = clipboardContent;
        _selectionContent = selectionContent;
        
        InitializeComponent();
        
        // Set the text for the menu items
        ClipboardText.Text = string.IsNullOrEmpty(clipboardContent) 
            ? "Clipboard: (empty)" 
            : $"Clipboard: {TruncateText(clipboardContent, 30)}";
            
        SelectionText.Text = string.IsNullOrEmpty(selectionContent) 
            ? "Selection: (empty)" 
            : $"Selection: {TruncateText(selectionContent, 30)}";
    }

    private static string TruncateText(string text, int maxLength)
    {
        if (text.Length <= maxLength)
            return text;
        return text.Substring(0, maxLength) + "...";
    }

    private void OnMenuItemEnter(object? sender, PointerEventArgs e)
    {
        if (sender is Border border)
        {
            border.Background = new SolidColorBrush(Color.Parse("#3E3E42"));
        }
    }

    private void OnMenuItemExit(object? sender, PointerEventArgs e)
    {
        if (sender is Border border)
        {
            border.Background = Brushes.Transparent;
        }
    }

    private void OnClipboardItemClick(object? sender, PointerPressedEventArgs e)
    {
        // For now, just show a message - this is where you'd implement actual functionality
        System.Diagnostics.Debug.WriteLine($"Clipboard item clicked: {_clipboardContent}");
        Close();
    }

    private void OnSelectionItemClick(object? sender, PointerPressedEventArgs e)
    {
        // For now, just show a message - this is where you'd implement actual functionality
        System.Diagnostics.Debug.WriteLine($"Selection item clicked: {_selectionContent}");
        Close();
    }
}
