using Avalonia.Controls;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Core.Note;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class VocabEditorDialog : Window
{
    public VocabEditorDialog()
    {
        InitializeComponent();
    }

    public VocabEditorDialog(VocabNote vocab) : this()
    {
        var viewModel = new VocabEditorViewModel(vocab);
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
