using System.Threading;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Manages the task progress dialog's view model tree and visibility lifecycle.
/// <see cref="TaskRunner"/> delegates all presentation concerns here:
/// showing/hiding the dialog, adding/removing scope VMs, and creating
/// <see cref="ScopeProgressPresenter"/>s for individual task runners.
/// </summary>
class DialogProgressPresenter
{
   readonly IUIThreadDispatcher _dispatcher;
   int _openScopes;

   /// <summary>Root view model for the task progress dialog. The UI layer observes this to manage dialog visibility and content.</summary>
   internal TaskProgressDialogViewModel DialogViewModel { get; } = new();

   internal DialogProgressPresenter(IUIThreadDispatcher dispatcher)
   {
      _dispatcher = dispatcher;
      dispatcher.OnTaskRunnerInstantiated(DialogViewModel);
   }

   internal void ShowDialog()
   {
      if(Interlocked.Increment(ref _openScopes) == 1)
         _dispatcher.InvokeSynchronouslyOnUIThread(() => DialogViewModel.IsVisible = true);
   }

   internal void HideDialogIfNoOpenScopes()
   {
      if(Interlocked.Decrement(ref _openScopes) == 0)
         _dispatcher.PostToUIThread(() => DialogViewModel.IsVisible = false);
   }

   internal TaskProgressScopeViewModel AddScope(string scopeTitle, int depth, TaskProgressScopeViewModel? parentScopeViewModel)
   {
      var viewModel = new TaskProgressScopeViewModel(scopeTitle, depth);
      if(parentScopeViewModel != null)
         _dispatcher.InvokeSynchronouslyOnUIThread(() => parentScopeViewModel.Children.Add(viewModel));
      else
         _dispatcher.InvokeSynchronouslyOnUIThread(() => DialogViewModel.RootScopes.Add(viewModel));

      return viewModel;
   }

   internal void RemoveScope(TaskProgressScopeViewModel scopeViewModel, TaskProgressScopeViewModel? parentScopeViewModel)
   {
      scopeViewModel.Dispose();
      if(parentScopeViewModel != null)
         _dispatcher.PostToUIThread(() => parentScopeViewModel.Children.Remove(scopeViewModel));
      else
         _dispatcher.PostToUIThread(() => DialogViewModel.RootScopes.Remove(scopeViewModel));
   }

   internal ScopeProgressPresenter CreateScopePresenter(TaskProgressScopeViewModel scopeViewModel, bool allowCancel) =>
      new(scopeViewModel, _dispatcher, allowCancel);
}
