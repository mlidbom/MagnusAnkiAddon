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
        DataContext = new VocabFlagsViewModel(vocab);
    }
}
