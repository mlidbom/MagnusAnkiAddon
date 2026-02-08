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

   /// <summary>
   /// The one and only way to obtain a task runner.
   /// Returns a scope that implements <see cref="ITaskProgressRunner"/>.
   /// Every method call on the scope creates its own progress panel, runs the work,
   /// and removes the panel when done. Concurrent calls display stacked panels.
   /// </summary>
   public ITaskProgressRunner Current(string windowTitle, bool forceHide = false, bool allowCancel = true, bool modal = false) =>
      new TaskRunnerScope(this, windowTitle, forceHide, allowCancel, modal);
}

/// <summary>
/// A scoped task runner obtained from <see cref="TaskRunner.Current"/>.
/// Implements <see cref="ITaskProgressRunner"/> — every method call creates its own
/// progress panel for the duration of that call then removes it. This means
/// concurrent calls (sync or async) each get their own panel automatically.
/// </summary>
public class TaskRunnerScope : ITaskProgressRunner
{
   readonly TaskRunner _taskRunner;
   readonly string _windowTitle;
   readonly bool _visible;
   readonly bool _allowCancel;
   readonly bool _modal;

   internal TaskRunnerScope(TaskRunner taskRunner, string windowTitle, bool forceHide, bool allowCancel, bool modal)
   {
      _taskRunner = taskRunner;
      _windowTitle = windowTitle;
      _allowCancel = allowCancel;
      _modal = modal;
      _visible = !App.IsTesting && !forceHide;
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

   public async Task<TResult> RunOnBackgroundThreadAsync<TResult>(string message, Func<TResult> action)
   {
      using var runner = CreateRunner(message);
      return await runner.RunOnBackgroundThreadAsync(message, action);
   }

   public void SetLabelText(string text)
   { /* No persistent panel — each method manages its own */
   }

   public void RunGc()
   { /* No-op in C# */
   }

   public bool IsHidden() => !_visible;
   public void Close() {}
   public void Dispose() {}
}
