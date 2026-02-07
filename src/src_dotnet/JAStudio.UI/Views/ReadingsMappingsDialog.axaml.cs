using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class ReadingsMappingsDialog : Window
{
    public ReadingsMappingsDialog(Core.TemporaryServiceCollection services)
    {
        InitializeComponent();
        DataContext = new ReadingsMappingsDialogViewModel(this, services);
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }
}
