using Avalonia.Threading;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// Adapts <see cref="TaskProgressScopeViewModel"/> (Core) and
/// <see cref="TaskProgressScopePanel"/> (Avalonia) to <see cref="IScopePanel"/> (Core).
/// </summary>
public class AvaloniaScopePanel : IScopePanel
{
   readonly TaskProgressScopeViewModel _viewModel;
   readonly TaskProgressScopePanel _panel;

   public AvaloniaScopePanel(TaskProgressScopeViewModel viewModel, TaskProgressScopePanel panel)
   {
      _viewModel = viewModel;
      _panel = panel;
   }

   public TaskProgressScopeViewModel ViewModel => _viewModel;

   public string GetFinalElapsed() => _viewModel.GetFinalElapsed();

   public void Dispose()
   {
      _viewModel.Dispose();
      Dispatcher.UIThread.Post(() => MultiTaskProgressDialog.RemoveScopePanel(_panel));
   }
}
