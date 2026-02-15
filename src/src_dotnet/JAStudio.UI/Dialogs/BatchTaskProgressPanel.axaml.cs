using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// A progress panel for batch/determinate operations that process a collection of items.
/// Bound to a <see cref="BatchTaskProgressViewModel"/>.
/// </summary>
public partial class BatchTaskProgressPanel : UserControl
{
   public BatchTaskProgressPanel()
   {
      InitializeComponent();
   }

   void InitializeComponent()
   {
      AvaloniaXamlLoader.Load(this);
   }

   void OnCancelClick(object? sender, RoutedEventArgs e)
   {
      (DataContext as TaskProgressViewModel)?.RequestCancel();
   }
}
