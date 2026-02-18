using System.Threading;

namespace JAStudio.Core.TaskRunners;

public class TaskRunner
{
   readonly IUIThreadDispatcher _dispatcher;

   /// <summary>Root view model for the task progress dialog. The UI layer observes this to manage dialog visibility and content. </summary>
   internal TaskProgressDialogViewModel DialogViewModel { get; } = new();

   internal TaskRunner(IUIThreadDispatcher dispatcher)
   {
      _dispatcher = dispatcher;
      dispatcher.OnTaskRunnerInstantiated(DialogViewModel);
   }

   internal ITaskProgressRunner CreateRunner(TaskProgressScopeViewModel? scopeViewModel, string labelText, bool? visible = null, bool allowCancel = true)
   {
      visible ??= !CoreApp.IsTesting;

      if(!visible.Value || scopeViewModel == null)
      {
         return new InvisibleTaskRunner(labelText);
      }

      var presenter = new ScopeProgressPresenter(scopeViewModel, _dispatcher, allowCancel);
      return new VisibleTaskRunner(presenter, allowCancel);
   }

   internal TaskProgressScopeViewModel? CreateScopeViewModel(string scopeTitle, bool visible, int depth)
   {
      if(!visible) return null;

      var viewmodel = new TaskProgressScopeViewModel(scopeTitle, depth);
      var parentViewmodel = _parentScopeViewmodel.Value;
      if(parentViewmodel != null)
      {
         _dispatcher.InvokeSynchronouslyOnUIThread(() => parentViewmodel.Children.Add(viewmodel));
      } else
      {
         _dispatcher.InvokeSynchronouslyOnUIThread(() => DialogViewModel.RootScopes.Add(viewmodel));
      }

      return viewmodel;
   }

   /// <summary>Tracks the number of currently open scopes across all threads. Used solely for dialog lifetime management (show/hide). Thread-safe via <see cref="Interlocked"/>.</summary>
   int _openScopes;

   /// <summary>Tracks the logical nesting depth per async call chain. Parallel siblings calling <see cref="Current"/> from the same parent scope each inherit the parent's depth and thus land at the same visual level.</summary>
   readonly AsyncLocal<int> _nestingDepth = new();

   /// <summary>Tracks the current parent scope view model per async call chain so that child scopes are nested inside their parent rather than appended to the top-level dialog. </summary>
   readonly AsyncLocal<TaskProgressScopeViewModel?> _parentScopeViewmodel = new();

   /// <summary>Tracks the current log entry per async call chain so that child scopes and tasks can attach their log entries to the parent. </summary>
   readonly AsyncLocal<TaskLogEntry?> _currentLogEntry = new();

   /// <summary>Returns a scope that implements <see cref="ITaskProgressRunner"/>. Nested calls share the same progress dialog window which stays open and in place until the outermost scope is disposed.
   /// Each individual method call on the scope gets its own progress panel within that dialog. Each scope gets its own heading panel and logs its total elapsed time.</summary>
   public ITaskProgressRunner Current(string scopeTitle, bool forceHide = false, bool allowCancel = true)
   {
      var visible = !CoreApp.IsTesting && !forceHide;

      var previousNestingDepth = _nestingDepth.Value;
      var depth = previousNestingDepth + 1;
      _nestingDepth.Value = depth;

      if(Interlocked.Increment(ref _openScopes) == 1 && visible)
      {
         _dispatcher.InvokeSynchronouslyOnUIThread(() => DialogViewModel.IsVisible = true);
      }

      var scope = new TaskRunnerScope(this, scopeTitle, visible, allowCancel, depth, previousNestingDepth, _parentScopeViewmodel.Value, _currentLogEntry.Value);
      _parentScopeViewmodel.Value = scope.ScopeViewModel;
      _currentLogEntry.Value = scope.LogEntry;
      return scope;
   }

   internal void OnScopeDisposed(TaskProgressScopeViewModel? disposedScopeVM, int previousNestingDepth, TaskProgressScopeViewModel? previousParentScopeVM, TaskLogEntry? previousLogEntry)
   {
      if(disposedScopeVM != null)
      {
         disposedScopeVM.Dispose();
         if(previousParentScopeVM != null)
            _dispatcher.PostToUIThread(() => previousParentScopeVM.Children.Remove(disposedScopeVM));
         else
            _dispatcher.PostToUIThread(() => DialogViewModel.RootScopes.Remove(disposedScopeVM));
      }

      _nestingDepth.Value = previousNestingDepth;
      _parentScopeViewmodel.Value = previousParentScopeVM;
      _currentLogEntry.Value = previousLogEntry;

      if(Interlocked.Decrement(ref _openScopes) == 0)
      {
         _dispatcher.PostToUIThread(() => DialogViewModel.IsVisible = false);
      }
   }
}
