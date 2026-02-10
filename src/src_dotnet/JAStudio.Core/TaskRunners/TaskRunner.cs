using System;
using System.Collections.Generic;
using System.Threading.Tasks;
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

/// <summary>
/// A scoped task runner obtained from <see cref="TaskRunner.Current"/>.
/// Each method call creates its own progress panel for the duration of that call.
/// The dialog window is held open by <see cref="TaskRunner"/> from the outermost
/// scope until it is disposed, so panels can come and go without the window
/// flickering or repositioning.
/// </summary>
public class TaskRunnerScope : ITaskProgressRunner
{
   readonly TaskRunner _taskRunner;
   readonly string _windowTitle;
   readonly bool _visible;
   readonly bool _allowCancel;
   readonly bool _modal;
   bool _disposed;

   internal TaskRunnerScope(TaskRunner taskRunner, string windowTitle, bool visible, bool allowCancel, bool modal)
   {
      _taskRunner = taskRunner;
      _windowTitle = windowTitle;
      _allowCancel = allowCancel;
      _modal = modal;
      _visible = visible;
   }

   ITaskProgressRunner CreateRunner(string message) => _taskRunner.Create(_windowTitle, message, _visible, _allowCancel, _modal);

   public List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      using var runner = CreateRunner(message);
      return runner.ProcessWithProgress(items, processItem, message, threads);
   }

   public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action)
   {
      using var runner = CreateRunner(message);
      return runner.RunOnBackgroundThreadWithSpinningProgressDialog(message, action);
   }

   public async Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threadCount)
   {
      using var runner = CreateRunner(message);
      return await runner.ProcessWithProgressAsync(items, processItem, message, threadCount);
   }

   public async Task<TResult> RunOnBackgroundThreadWithSpinningProgressDialogAsync<TResult>(string message, Func<TResult> action)
   {
      using var runner = CreateRunner(message);
      return await runner.RunOnBackgroundThreadWithSpinningProgressDialogAsync(message, action);
   }

   public void SetLabelText(string text)
   { /* No persistent panel — each method manages its own */
   }

   public bool IsHidden() => !_visible;

   public void Close() => Dispose();

   public void Dispose()
   {
      if(_disposed) return;
      _disposed = true;
      _taskRunner.OnScopeDisposed();
   }
}
