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
    public static void Hold()
    {
        Dispatcher.UIThread.VerifyAccess();
        _holdCount++;
        EnsureVisible();
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
    /// Create a new scope panel and add it to the shared dialog.
    /// Opens the dialog if it is not already visible.
    /// Must be called on the UI thread.
    /// </summary>
    public static TaskProgressScopePanel CreateScopePanel(string scopeTitle, int depth)
    {
        Dispatcher.UIThread.VerifyAccess();
        EnsureVisible();

        var scopePanel = new TaskProgressScopePanel(depth);
        scopePanel.SetHeading(scopeTitle);
        _instance!.Container.Children.Add(scopePanel);
        return scopePanel;
    }

    /// <summary>
    /// Remove a scope panel from the shared dialog.
    /// Closes the dialog when the last panel is removed and no holds are active.
    /// Must be called on the UI thread.
    /// </summary>
    public static void RemoveScopePanel(TaskProgressScopePanel scopePanel)
    {
        Dispatcher.UIThread.VerifyAccess();

        if (_instance == null) return;

        _instance.Container.Children.Remove(scopePanel);
        CloseIfEmpty();
    }

    static void EnsureVisible()
    {
        if (_instance == null || !_instance.IsVisible)
        {
            _instance = new MultiTaskProgressDialog();
            WindowPositioner.PositionNearCursor(_instance);
            _instance.Show();
        }
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
