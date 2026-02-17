using System.Threading;

namespace JAStudio.Core.TaskRunners;

public class TaskRunner
{
   readonly ITaskProgressUI _progressUI;

   internal TaskRunner(ITaskProgressUI progressUI) => _progressUI = progressUI;

   internal ITaskProgressRunner Create(IScopePanel? scopePanel, string labelText, bool? visible = null, bool allowCancel = true)
   {
      visible ??= !CoreApp.IsTesting;

      if(!visible.Value || scopePanel == null)
      {
         return new InvisibleTaskRunner(labelText);
      }

      return _progressUI.CreateTaskRunner(scopePanel, labelText, allowCancel);
   }

   internal IScopePanel? CreateScopePanel(string scopeTitle, bool visible, int depth)
   {
      if(!visible) return null;

      return _progressUI.CreateScopePanel(scopeTitle, depth, _parentScope.Value);
   }

   /// <summary>
   /// Tracks the number of currently open scopes across all threads.
   /// Used solely for dialog lifetime management (hold/release).
   /// Thread-safe via <see cref="Interlocked"/>.
   /// </summary>
   int _openScopes;

   /// <summary>
   /// Tracks the logical nesting depth per async call chain.
   /// Parallel siblings calling <see cref="Current"/> from the same parent scope
   /// each inherit the parent's depth and thus land at the same visual level.
   /// </summary>
   readonly AsyncLocal<int> _nestingDepth = new();

   /// <summary>
   /// Tracks the current parent scope panel per async call chain so that
   /// child scopes are nested inside their parent rather than appended
   /// to the top-level dialog.
   /// </summary>
   readonly AsyncLocal<IScopePanel?> _parentScope = new();

   /// <summary>
   /// Tracks the current log entry per async call chain so that
   /// child scopes and tasks can attach their log entries to the parent.
   /// </summary>
   readonly AsyncLocal<TaskLogEntry?> _currentLogEntry = new();

   /// <summary>
   /// The one and only way to obtain a task runner.
   /// Returns a scope that implements <see cref="ITaskProgressRunner"/>.
   /// Nested calls share the same progress dialog window which stays open and
   /// in place until the outermost scope is disposed. Each individual method
   /// call on the scope gets its own progress panel within that dialog.
   /// Each scope gets its own heading panel and logs its total elapsed time.
   /// </summary>
   public ITaskProgressRunner Current(string scopeTitle, bool forceHide = false, bool allowCancel = true)
   {
      var visible = !CoreApp.IsTesting && !forceHide;

      var previousNestingDepth = _nestingDepth.Value;
      var depth = previousNestingDepth + 1;
      _nestingDepth.Value = depth;

      if(Interlocked.Increment(ref _openScopes) == 1 && visible)
      {
         _progressUI.HoldDialog();
      }

      var scope = new TaskRunnerScope(this, scopeTitle, visible, allowCancel, depth, previousNestingDepth, _parentScope.Value, _currentLogEntry.Value);
      _parentScope.Value = scope.ScopePanel;
      _currentLogEntry.Value = scope.LogEntry;
      return scope;
   }

   internal void OnScopeDisposed(int previousNestingDepth, IScopePanel? previousParentScope, TaskLogEntry? previousLogEntry)
   {
      _nestingDepth.Value = previousNestingDepth;
      _parentScope.Value = previousParentScope;
      _currentLogEntry.Value = previousLogEntry;

      if(Interlocked.Decrement(ref _openScopes) == 0)
      {
         _progressUI.ReleaseDialog();
      }
   }
}
