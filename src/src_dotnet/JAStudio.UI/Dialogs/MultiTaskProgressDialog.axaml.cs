using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using Avalonia.Threading;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// A shared dialog window that hosts one or more <see cref="TaskProgressPanel"/> instances
/// in a vertical stack. Created automatically when the first panel is requested and
/// closed when the last panel is removed.
/// All public static methods must be called on the Avalonia UI thread.
/// </summary>
public partial class MultiTaskProgressDialog : Window
{
    static MultiTaskProgressDialog? _instance;
    static int _holdCount;

    public MultiTaskProgressDialog()
    {
        InitializeComponent();
    }

    void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    StackPanel Container => this.FindControl<StackPanel>("PanelContainer")!;

    /// <summary>
    /// Hold the dialog open even when all panels have been removed.
    /// Call once when the outermost task scope is entered.
    /// Must be called on the UI thread.
    /// </summary>
    public static void Hold(string windowTitle)
    {
        Dispatcher.UIThread.VerifyAccess();
        _holdCount++;
        if (_instance == null || !_instance.IsVisible)
        {
            _instance = new MultiTaskProgressDialog { Title = windowTitle };
            WindowPositioner.PositionNearCursor(_instance);
            _instance.Show();
        }
    }

    /// <summary>
    /// Release a hold. When the hold count reaches zero and no panels remain,
    /// the dialog is closed.
    /// Must be called on the UI thread.
    /// </summary>
    public static void Release()
    {
        Dispatcher.UIThread.VerifyAccess();
        _holdCount--;
        CloseIfEmpty();
    }

    /// <summary>
    /// Create a new progress panel and add it to the shared dialog.
    /// Opens the dialog if it is not already visible.
    /// Must be called on the UI thread.
    /// </summary>
    public static TaskProgressPanel CreatePanel(string windowTitle, string message, bool allowCancel)
    {
        Dispatcher.UIThread.VerifyAccess();

        if (_instance == null || !_instance.IsVisible)
        {
            _instance = new MultiTaskProgressDialog { Title = windowTitle };
            WindowPositioner.PositionNearCursor(_instance);
            _instance.Show();
        }

        var panel = new TaskProgressPanel();
        panel.SetMessage(message);
        panel.ShowCancelButton(allowCancel);
        _instance.Container.Children.Add(panel);

        return panel;
    }

    /// <summary>
    /// Remove a panel from the shared dialog.
    /// Closes the dialog when the last panel is removed and no holds are active.
    /// Must be called on the UI thread.
    /// </summary>
    public static void RemovePanel(TaskProgressPanel panel)
    {
        Dispatcher.UIThread.VerifyAccess();

        if (_instance == null) return;

        _instance.Container.Children.Remove(panel);
        CloseIfEmpty();
    }

    static void CloseIfEmpty()
    {
        if (_instance != null && _holdCount <= 0 && _instance.Container.Children.Count == 0)
        {
            _instance.Close();
            _instance = null;
        }
    }
}
