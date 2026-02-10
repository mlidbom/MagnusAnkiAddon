using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using Avalonia.Threading;

namespace JAStudio.UI.Dialogs;

public partial class TaskProgressDialog : Window
{
    private bool _wasCanceled;

    public bool WasCanceled => _wasCanceled;

    public TaskProgressDialog()
    {
        InitializeComponent();
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public void SetTitle(string title)
    {
        Dispatcher.UIThread.Post(() => Title = title);
    }

    public void SetMessage(string message)
    {
        Dispatcher.UIThread.Post(() =>
        {
            var label = this.FindControl<TextBlock>("MessageLabel");
            if (label != null)
                label.Text = message;
        });
    }

    public void SetIndeterminate(bool indeterminate)
    {
        Dispatcher.UIThread.Post(() =>
        {
            var progressBar = this.FindControl<ProgressBar>("ProgressBar");
            if (progressBar != null)
                progressBar.IsIndeterminate = indeterminate;
        });
    }

    public void SetProgress(int current, int total)
    {
        Dispatcher.UIThread.Post(() =>
        {
            var progressBar = this.FindControl<ProgressBar>("ProgressBar");
            if (progressBar != null)
            {
                progressBar.IsIndeterminate = false;
                progressBar.Maximum = total;
                progressBar.Value = current;
            }
        });
    }

    public void ShowCancelButton(bool show)
    {
        Dispatcher.UIThread.Post(() =>
        {
            var cancelButton = this.FindControl<Button>("CancelButton");
            if (cancelButton != null)
                cancelButton.IsVisible = show;
        });
    }

    private void OnCancelClick(object? sender, RoutedEventArgs e)
    {
        _wasCanceled = true;
    }
}
