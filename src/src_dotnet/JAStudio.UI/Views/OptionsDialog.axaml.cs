using Avalonia.Controls;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class OptionsDialog : Window
{
    public OptionsDialog(Core.TemporaryServiceCollection services)
    {
        JALogger.Log("OptionsDialog constructor: calling InitializeComponent()...");
        InitializeComponent();
        JALogger.Log("OptionsDialog constructor: creating ViewModel...");
        DataContext = new OptionsDialogViewModel(this, services);
        JALogger.Log("OptionsDialog constructor: completed");
    }
}
