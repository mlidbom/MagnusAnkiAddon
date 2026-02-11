using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace JAStudio.Core.TaskRunners;

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
