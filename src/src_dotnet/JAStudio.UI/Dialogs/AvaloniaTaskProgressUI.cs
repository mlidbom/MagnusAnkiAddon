using Avalonia.Threading;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// Avalonia implementation of <see cref="ITaskProgressUI"/>.
/// Creates scope panels and task runners backed by the shared <see cref="MultiTaskProgressDialog"/>.
/// </summary>
class AvaloniaTaskProgressUI : ITaskProgressUI
{
   public IScopePanel CreateScopePanel(string scopeTitle, int depth, IScopePanel? parentScope)
   {
      var viewModel = new TaskProgressScopeViewModel(scopeTitle, depth);
      if(parentScope != null)
      {
         Dispatcher.UIThread.Invoke(() => parentScope.ViewModel.Children.Add(viewModel));
         return new AvaloniaScopePanel(viewModel, topLevelPanel: null, parentScope);
      }

      var panel = Dispatcher.UIThread.Invoke(() => MultiTaskProgressDialog.CreateScopePanel(viewModel, depth));
      return new AvaloniaScopePanel(viewModel, panel, parentScope: null);
   }

   public ITaskProgressRunner CreateTaskRunner(IScopePanel scopePanel, string labelText, bool allowCancel)
   {
      var avaloniaScope = (AvaloniaScopePanel)scopePanel;
      return new AvaloniaTaskProgressRunner(avaloniaScope.ViewModel, labelText, allowCancel);
   }

   public void HoldDialog() => Dispatcher.UIThread.Invoke(MultiTaskProgressDialog.Hold);

   public void ReleaseDialog() => Dispatcher.UIThread.Post(MultiTaskProgressDialog.Release);
}
