using Avalonia.Controls;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class OptionsDialog : Window
{
    public OptionsDialog()
    {
        JALogger.Log("OptionsDialog constructor: calling InitializeComponent()...");
        InitializeComponent();
        JALogger.Log("OptionsDialog constructor: creating ViewModel...");
        DataContext = new OptionsDialogViewModel(this);
        JALogger.Log("OptionsDialog constructor: completed");
    }
}
