using System;
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
    static readonly string[] DepthBackgrounds = ["#10808080", "#08606080", "#06404060", "#04303050"];

    readonly Stopwatch _stopwatch = Stopwatch.StartNew();
    DispatcherTimer? _timer;

    public TaskProgressScopePanel() : this(1) { }

    public TaskProgressScopePanel(int depth)
    {
        InitializeComponent();
        ApplyDepthStyling(depth);
        StartElapsedTimer();
    }

    void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    void ApplyDepthStyling(int depth)
    {
        // depth 1 = outermost scope, indent increases with depth
        var indent = Math.Max(0, (depth - 1) * 16);
        Margin = new Avalonia.Thickness(indent, 2, 0, 2);

        var border = this.FindControl<Border>("ScopeBorder");
        if (border != null)
        {
            var bgIndex = Math.Min(depth - 1, DepthBackgrounds.Length - 1);
            border.Background = Avalonia.Media.Brush.Parse(DepthBackgrounds[Math.Max(0, bgIndex)]);
        }
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
