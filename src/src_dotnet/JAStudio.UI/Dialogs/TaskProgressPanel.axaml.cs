using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// An embeddable progress panel bound to a <see cref="TaskProgressViewModel"/>.
/// All UI state is driven by data binding; no <c>FindControl</c> calls needed.
/// </summary>
public partial class TaskProgressPanel : UserControl
{
    public TaskProgressPanel()
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
