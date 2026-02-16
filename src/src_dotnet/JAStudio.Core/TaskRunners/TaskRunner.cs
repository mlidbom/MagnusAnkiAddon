using System;
using System.Threading;
using JAStudio.Core.Configuration;

namespace JAStudio.Core.TaskRunners;

public class TaskRunner
{
   internal TaskRunner(JapaneseConfig _) {}

   Func<string, int, IScopePanel?, IScopePanel>? _uiScopePanelFactory;
   Func<IScopePanel, string, bool, ITaskProgressRunner>? _uiTaskRunnerFactory;

   /// <summary>
   /// Register the factory that creates a visible <see cref="ITaskProgressRunner"/>
   /// whose child panels live inside the given <see cref="IScopePanel"/>.
   /// </summary>
   public void SetUiTaskRunnerFactory(Func<IScopePanel, string, bool, ITaskProgressRunner> factory)
   {
      if(_uiTaskRunnerFactory != null)
      {
         throw new InvalidOperationException("UI task runner factory already set.");
      }

      _uiTaskRunnerFactory = factory;
   }

   /// <summary>
   /// Register the factory that creates a scope-level panel in the UI.
   /// The panel shows a heading and elapsed time for the scope.
   /// Parameters: (scopeTitle, nestingDepth, parentScopePanel) → IScopePanel
   /// </summary>
   public void SetUiScopePanelFactory(Func<string, int, IScopePanel?, IScopePanel> factory)
   {
      if(_uiScopePanelFactory != null)
      {
         throw new InvalidOperationException("UI scope panel factory already set.");
      }

      _uiScopePanelFactory = factory;
   }

   Action? _holdDialog;
   Action? _releaseDialog;

   public void SetDialogLifetimeCallbacks(Action hold, Action release)
   {
      _holdDialog = hold;
      _releaseDialog = release;
   }

   internal ITaskProgressRunner Create(IScopePanel? scopePanel, string labelText, bool? visible = null, bool allowCancel = true)
   {
      visible ??= !App.IsTesting;

      if(!visible.Value || scopePanel == null)
      {
         return new InvisibleTaskRunner(labelText);
      }

      if(_uiTaskRunnerFactory == null)
      {
         throw new InvalidOperationException("No UI task runner factory set. Set it with TaskRunner.SetUiTaskRunnerFactory().");
      }

      return _uiTaskRunnerFactory(scopePanel, labelText, allowCancel);
   }

   internal IScopePanel? CreateScopePanel(string scopeTitle, bool visible, int depth)
   {
      if(!visible) return null;

      if(_uiScopePanelFactory == null)
      {
         throw new InvalidOperationException("No UI scope panel factory set. Set it with TaskRunner.SetUiScopePanelFactory().");
      }

      return _uiScopePanelFactory(scopeTitle, depth, _parentScope.Value);
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
   /// The one and only way to obtain a task runner.
   /// Returns a scope that implements <see cref="ITaskProgressRunner"/>.
   /// Nested calls share the same progress dialog window which stays open and
   /// in place until the outermost scope is disposed. Each individual method
   /// call on the scope gets its own progress panel within that dialog.
   /// Each scope gets its own heading panel and logs its total elapsed time.
   /// </summary>
   public ITaskProgressRunner Current(string scopeTitle, bool forceHide = false, bool allowCancel = true)
   {
      var visible = !App.IsTesting && !forceHide;

      var previousNestingDepth = _nestingDepth.Value;
      var depth = previousNestingDepth + 1;
      _nestingDepth.Value = depth;

      if(Interlocked.Increment(ref _openScopes) == 1 && visible)
      {
         _holdDialog?.Invoke();
      }

      var scope = new TaskRunnerScope(this, scopeTitle, visible, allowCancel, depth, previousNestingDepth, _parentScope.Value);
      _parentScope.Value = scope.ScopePanel;
      return scope;
   }

   internal void OnScopeDisposed(int previousNestingDepth, IScopePanel? previousParentScope)
   {
      _nestingDepth.Value = previousNestingDepth;
      _parentScope.Value = previousParentScope;

      if(Interlocked.Decrement(ref _openScopes) == 0)
      {
         _releaseDialog?.Invoke();
      }
   }
}
