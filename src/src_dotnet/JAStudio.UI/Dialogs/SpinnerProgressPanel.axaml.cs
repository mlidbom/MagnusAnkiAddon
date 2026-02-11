using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// A minimal progress panel for indeterminate/spinner operations.
/// Bound to a <see cref="TaskProgressViewModel"/>.
/// </summary>
public partial class SpinnerProgressPanel : UserControl
{
    public SpinnerProgressPanel()
    {
        InitializeComponent();
    }

    void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    void OnCancelClick(object? sender, RoutedEventArgs e)
    {
        (DataContext as TaskProgressViewModel)?.RequestCancel();
    }
}
