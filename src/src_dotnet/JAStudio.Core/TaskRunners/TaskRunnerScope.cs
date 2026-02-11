using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using Compze.Utilities.Logging;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// A scoped task runner obtained from <see cref="TaskRunner.Current"/>.
/// Each method call creates its own progress panel for the duration of that call.
/// The scope itself owns a <see cref="IScopePanel"/> that displays a heading
/// and elapsed time, and logs total elapsed time on dispose.
/// The dialog window is held open by <see cref="TaskRunner"/> from the outermost
/// scope until it is disposed, so panels can come and go without the window
/// flickering or repositioning.
/// </summary>
public class TaskRunnerScope : ITaskProgressRunner
{
   readonly TaskRunner _taskRunner;
   readonly string _scopeTitle;
   readonly bool _visible;
   readonly bool _allowCancel;
   readonly Stopwatch _stopwatch = Stopwatch.StartNew();
   readonly IScopePanel? _scopePanel;
   bool _disposed;

   internal TaskRunnerScope(TaskRunner taskRunner, string scopeTitle, bool visible, bool allowCancel)
   {
      _taskRunner = taskRunner;
      _scopeTitle = scopeTitle;
      _allowCancel = allowCancel;
      _visible = visible;
      _scopePanel = visible ? taskRunner.CreateScopePanel(scopeTitle, visible) : null;
   }

   ITaskProgressRunner CreateRunner(string message) => _taskRunner.Create(_scopePanel, message, _visible, _allowCancel);

   public List<TOutput> RunBatch<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      using var runner = CreateRunner(message);
      return runner.RunBatch(items, processItem, message, threads);
   }

   public TResult RunIndeterminate<TResult>(string message, Func<TResult> action)
   {
      using var runner = CreateRunner(message);
      return runner.RunIndeterminate(message, action);
   }

   public async Task<List<TOutput>> RunBatchAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threadCount)
   {
      using var runner = CreateRunner(message);
      return await runner.RunBatchAsync(items, processItem, message, threadCount);
   }

   public async Task<TResult> RunIndeterminateAsync<TResult>(string message, Func<TResult> action)
   {
      using var runner = CreateRunner(message);
      return await runner.RunIndeterminateAsync(message, action);
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

      _stopwatch.Stop();
      this.Log().Info($"Scope \"{_scopeTitle}\" completed in {_stopwatch.Elapsed:g}");

      _scopePanel?.Dispose();
      _taskRunner.OnScopeDisposed();
   }
}
