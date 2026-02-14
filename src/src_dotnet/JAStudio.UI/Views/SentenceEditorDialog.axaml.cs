using Avalonia.Controls;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Anki;
using JAStudio.Core.Note;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class SentenceEditorDialog : Window
{
    public SentenceEditorDialog()
    {
        InitializeComponent();
    }

    public SentenceEditorDialog(SentenceNote sentence) : this()
    {
        var viewModel = new SentenceEditorViewModel(sentence);

        viewModel.SaveCommand = new RelayCommand(() =>
        {
            viewModel.Save();
            AnkiFacade.UIUtils.Refresh();
            Close();
        });

        viewModel.CancelCommand = new RelayCommand(() =>
        {
            Close();
        });

        DataContext = viewModel;
    }
}
