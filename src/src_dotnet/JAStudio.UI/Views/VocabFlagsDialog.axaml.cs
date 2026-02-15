using Avalonia.Controls;
using JAStudio.Anki;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class VocabFlagsDialog : Window
{
   public VocabFlagsDialog()
   {
      InitializeComponent();
   }

   public VocabFlagsDialog(VocabNote vocab, Core.TemporaryServiceCollection services) : this()
   {
      var viewModel = new VocabFlagsViewModel(vocab, services, this);
      DataContext = viewModel;

      // Wire up commands to close the dialog
      viewModel.SaveCommand = new CommunityToolkit.Mvvm.Input.AsyncRelayCommand(async () =>
      {
         await viewModel.SaveAsync();
         AnkiFacade.UIUtils.Refresh();
         Close();
      });

      viewModel.CancelCommand = new CommunityToolkit.Mvvm.Input.RelayCommand(Close);
   }
}
