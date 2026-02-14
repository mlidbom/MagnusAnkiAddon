using Avalonia.Controls;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Core.Note;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class KanjiEditorDialog : Window
{
    public KanjiEditorDialog()
    {
        InitializeComponent();
    }

    public KanjiEditorDialog(KanjiNote kanji) : this()
    {
        var viewModel = new KanjiEditorViewModel(kanji);
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
