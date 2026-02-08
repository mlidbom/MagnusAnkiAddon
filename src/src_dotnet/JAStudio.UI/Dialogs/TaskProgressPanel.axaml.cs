using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// An embeddable progress panel (message + progress bar + optional cancel).
/// Multiple panels are stacked inside <see cref="MultiTaskProgressDialog"/>
/// to show parallel task progress.
/// All public methods must be called on the Avalonia UI thread.
/// </summary>
public partial class TaskProgressPanel : UserControl
{
    volatile bool _wasCanceled;

    public bool WasCanceled => _wasCanceled;

    public TaskProgressPanel()
    {
        InitializeComponent();
    }

    void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public void SetMessage(string message)
    {
        var label = this.FindControl<TextBlock>("MessageLabel");
        if (label != null) label.Text = message;
    }

    public void SetIndeterminate(bool indeterminate)
    {
        var bar = this.FindControl<ProgressBar>("ProgressBar");
        if (bar != null) bar.IsIndeterminate = indeterminate;
    }

    public void SetProgress(int current, int total)
    {
        var bar = this.FindControl<ProgressBar>("ProgressBar");
        if (bar != null)
        {
            bar.IsIndeterminate = false;
            bar.Maximum = total;
            bar.Value = current;
        }
    }

    public void ShowCancelButton(bool show)
    {
        var btn = this.FindControl<Button>("CancelButton");
        if (btn != null) btn.IsVisible = show;
    }

    void OnCancelClick(object? sender, RoutedEventArgs e)
    {
        _wasCanceled = true;
    }
}
