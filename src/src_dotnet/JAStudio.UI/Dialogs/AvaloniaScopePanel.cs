using Avalonia.Threading;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// Adapts <see cref="TaskProgressScopeViewModel"/> (Core) and
/// <see cref="TaskProgressScopePanel"/> (Avalonia) to <see cref="IScopePanel"/> (Core).
/// When a parent scope exists, the view model is nested inside the parent's children
/// collection; otherwise a panel is added to the top-level dialog.
/// </summary>
class AvaloniaScopePanel : IScopePanel
{
   readonly TaskProgressScopePanel? _topLevelPanel;
   readonly IScopePanel? _parentScope;

   public AvaloniaScopePanel(TaskProgressScopeViewModel viewModel, TaskProgressScopePanel? topLevelPanel, IScopePanel? parentScope)
   {
      ViewModel = viewModel;
      _topLevelPanel = topLevelPanel;
      _parentScope = parentScope;
   }

   public TaskProgressScopeViewModel ViewModel { get; }

   public void Dispose()
   {
      ViewModel.Dispose();
      if(_parentScope != null)
      {
         Dispatcher.UIThread.Post(() => _parentScope.ViewModel.Children.Remove(ViewModel));
      } else if(_topLevelPanel != null)
      {
         Dispatcher.UIThread.Post(() => MultiTaskProgressDialog.RemoveScopePanel(_topLevelPanel));
      }
   }
}
