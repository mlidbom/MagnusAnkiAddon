using System;
using JAStudio.Core.Configuration;

namespace JAStudio.Core.TaskRunners;

public class TaskRunner
{
   readonly JapaneseConfig _config;
   internal TaskRunner(JapaneseConfig config) => _config = config;

   Func<string, string, bool, bool, ITaskProgressRunner>? _uiTaskRunnerFactory;

   public void SetUiTaskRunnerFactory(Func<string, string, bool, bool, ITaskProgressRunner> factory)
   {
      if(_uiTaskRunnerFactory != null)
      {
         throw new InvalidOperationException("UI task runner factory already set.");
      }

      _uiTaskRunnerFactory = factory;
   }

   Action<string>? _holdDialog;
   Action? _releaseDialog;

   public void SetDialogLifetimeCallbacks(Action<string> hold, Action release)
   {
      _holdDialog = hold;
      _releaseDialog = release;
   }

   internal ITaskProgressRunner Create(string windowTitle, string labelText, bool? visible = null, bool allowCancel = true, bool modal = false)
   {
      visible ??= !App.IsTesting;

      if(!visible.Value)
      {
         return new InvisibleTaskRunner(windowTitle, labelText);
      }

      if(_uiTaskRunnerFactory == null)
      {
         throw new InvalidOperationException("No UI task runner factory set. Set it with TaskRunner.SetUiTaskRunnerFactory().");
      }

      return _uiTaskRunnerFactory(windowTitle, labelText, allowCancel, modal);
   }

   int _depth;

   /// <summary>
   /// The one and only way to obtain a task runner.
   /// Returns a scope that implements <see cref="ITaskProgressRunner"/>.
   /// Nested calls share the same progress dialog window which stays open and
   /// in place until the outermost scope is disposed. Each individual method
   /// call on the scope gets its own progress panel within that dialog.
   /// </summary>
   public ITaskProgressRunner Current(string windowTitle, bool forceHide = false, bool allowCancel = true, bool modal = false)
   {
      var visible = !App.IsTesting && !forceHide;
      _depth++;
      if(_depth == 1 && visible)
      {
         _holdDialog?.Invoke(windowTitle);
      }

      return new TaskRunnerScope(this, windowTitle, visible, allowCancel, modal);
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