using System;
using System.Threading;
using JAStudio.Core.Configuration;

namespace JAStudio.Core.TaskRunners;

public class TaskRunner
{
   internal TaskRunner(JapaneseConfig _) { }

   Func<string, int, IScopePanel>? _uiScopePanelFactory;
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
   /// Parameters: (scopeTitle, nestingDepth) → IScopePanel
   /// </summary>
   public void SetUiScopePanelFactory(Func<string, int, IScopePanel> factory)
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

   internal IScopePanel? CreateScopePanel(string scopeTitle, bool visible)
   {
      if(!visible) return null;

      if(_uiScopePanelFactory == null)
      {
         throw new InvalidOperationException("No UI scope panel factory set. Set it with TaskRunner.SetUiScopePanelFactory().");
      }

      return _uiScopePanelFactory(scopeTitle, _depth);
   }

   int _depth;

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
      _depth++;
      if(_depth == 1 && visible)
      {
         _holdDialog?.Invoke();
      }

      return new TaskRunnerScope(this, scopeTitle, visible, allowCancel);
   }

   internal void OnScopeDisposed()
   {
      _depth--;
      if(_depth == 0)
      {
         _releaseDialog?.Invoke();
      }
   }
}