using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using Avalonia.Threading;

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
    /// Closes the dialog when the last panel is removed.
    /// Must be called on the UI thread.
    /// </summary>
    public static void RemovePanel(TaskProgressPanel panel)
    {
        Dispatcher.UIThread.VerifyAccess();

        if (_instance == null) return;

        _instance.Container.Children.Remove(panel);

        if (_instance.Container.Children.Count == 0)
        {
            _instance.Close();
            _instance = null;
        }
    }
}
