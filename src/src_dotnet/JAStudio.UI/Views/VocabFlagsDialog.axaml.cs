using Avalonia.Controls;
using JAStudio.Core.Note;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class VocabFlagsDialog : Window
{
    public VocabFlagsDialog()
    {
        InitializeComponent();
    }

    public VocabFlagsDialog(VocabNote vocab) : this()
    {
        var viewModel = new VocabFlagsViewModel(vocab, Core.TemporaryServiceCollection.Instance, this);
        DataContext = viewModel;

        // Wire up commands to close the dialog
        viewModel.SaveCommand = new CommunityToolkit.Mvvm.Input.AsyncRelayCommand(async () =>
        {
            await viewModel.SaveAsync();
            Close();
        });

        viewModel.CancelCommand = new CommunityToolkit.Mvvm.Input.RelayCommand(() =>
        {
            Close();
        });
    }
}
