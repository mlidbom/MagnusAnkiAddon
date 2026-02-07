using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Markup.Xaml;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class NoteSearchDialog : Window
{
    private static NoteSearchDialog? _instance;

    /// <summary>
    /// Get the singleton instance of the dialog.
    /// </summary>
    public static NoteSearchDialog Instance
    {
        get
        {
            if (_instance == null)
            {
                _instance = new NoteSearchDialog();
            }
            return _instance;
        }
    }

    public NoteSearchDialog()
    {
        InitializeComponent();
        DataContext = new NoteSearchDialogViewModel(Core.TemporaryServiceCollection.Instance);
        
        // Focus search input when dialog is shown
        Opened += (_, _) =>
        {
            var searchInput = this.FindControl<TextBox>("SearchInput");
            searchInput?.Focus();
        };
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    private void OnResultDoubleClick(object? sender, TappedEventArgs e)
    {
        var viewModel = DataContext as NoteSearchDialogViewModel;
        viewModel?.OpenSelectedNote();
    }

    /// <summary>
    /// Toggle the visibility of the dialog (show if hidden, hide if shown).
    /// </summary>
    public static void ToggleVisibility()
    {
        if (Instance.IsVisible)
        {
            Instance.Hide();
        }
        else
        {
            Instance.Show();
            Instance.Activate();
            var searchInput = Instance.FindControl<TextBox>("SearchInput");
            searchInput?.Focus();
        }
    }
}
