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

        UpdateStatsLabel(current, total, null, null, null);
    }

    public void SetTimeStats(string elapsed, string remaining, string estimatedTotal)
    {
        var bar = this.FindControl<ProgressBar>("ProgressBar");
        var current = bar != null ? (int)bar.Value : 0;
        var total = bar != null ? (int)bar.Maximum : 0;
        UpdateStatsLabel(current, total, elapsed, remaining, estimatedTotal);
    }

    void UpdateStatsLabel(int current, int total, string? elapsed, string? remaining, string? estimatedTotal)
    {
        var label = this.FindControl<TextBlock>("StatsLabel");
        if (label == null) return;

        var parts = new System.Collections.Generic.List<string> { $"{current}/{total}" };
        if (elapsed != null) parts.Add($"elapsed: {elapsed}");
        if (remaining != null) parts.Add($"remaining: {remaining}");
        if (estimatedTotal != null) parts.Add($"est: {estimatedTotal}");
        label.Text = string.Join("  \u2022  ", parts);
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
