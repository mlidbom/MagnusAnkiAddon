using System.Diagnostics;
using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using Avalonia.Threading;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// A scope-level panel that displays a heading and elapsed time,
/// and hosts child <see cref="TaskProgressPanel"/> instances for
/// individual operations within the scope.
/// All public methods must be called on the Avalonia UI thread.
/// </summary>
public partial class TaskProgressScopePanel : UserControl
{
    readonly Stopwatch _stopwatch = Stopwatch.StartNew();
    DispatcherTimer? _timer;

    public TaskProgressScopePanel()
    {
        InitializeComponent();
        StartElapsedTimer();
    }

    void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public void SetHeading(string text)
    {
        var heading = this.FindControl<TextBlock>("ScopeHeading");
        if (heading != null) heading.Text = text;
    }

    public TaskProgressPanel CreateChildPanel(string message, bool allowCancel)
    {
        var panel = new TaskProgressPanel();
        panel.SetMessage(message);
        panel.ShowCancelButton(allowCancel);
        var container = this.FindControl<StackPanel>("ChildPanelContainer")!;
        container.Children.Add(panel);
        return panel;
    }

    public void RemoveChildPanel(TaskProgressPanel panel)
    {
        var container = this.FindControl<StackPanel>("ChildPanelContainer");
        container?.Children.Remove(panel);
    }

    void StartElapsedTimer()
    {
        _timer = new DispatcherTimer { Interval = System.TimeSpan.FromSeconds(1) };
        _timer.Tick += (_, _) => UpdateElapsedLabel();
        _timer.Start();
    }

    void UpdateElapsedLabel()
    {
        var label = this.FindControl<TextBlock>("ElapsedLabel");
        if (label != null)
        {
            var elapsed = _stopwatch.Elapsed;
            label.Text = $"{elapsed.Hours:D2}:{elapsed.Minutes:D2}:{elapsed.Seconds:D2}";
        }
    }

    public string GetFinalElapsed()
    {
        _stopwatch.Stop();
        _timer?.Stop();
        var elapsed = _stopwatch.Elapsed;
        return $"{elapsed.Hours:D2}:{elapsed.Minutes:D2}:{elapsed.Seconds:D2}";
    }
}
