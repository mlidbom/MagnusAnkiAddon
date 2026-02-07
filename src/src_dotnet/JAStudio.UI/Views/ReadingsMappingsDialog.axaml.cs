using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class ReadingsMappingsDialog : Window
{
    public ReadingsMappingsDialog()
    {
        InitializeComponent();
        DataContext = new ReadingsMappingsDialogViewModel(this, Core.TemporaryServiceCollection.Instance);
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }
}
