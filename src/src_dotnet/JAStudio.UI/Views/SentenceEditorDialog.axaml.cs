using Avalonia.Controls;
using CommunityToolkit.Mvvm.Input;
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
        DataContext = viewModel;

        viewModel.SaveCommand = new RelayCommand(() =>
        {
            viewModel.Save();
            Close();
        });

        viewModel.CancelCommand = new RelayCommand(() =>
        {
            Close();
        });
    }
}
