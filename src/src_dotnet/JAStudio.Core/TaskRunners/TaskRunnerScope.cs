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
class TaskRunnerScope : ITaskProgressRunner
{
   readonly TaskRunner _taskRunner;
   readonly string _scopeTitle;
   readonly bool _visible;
   readonly bool _allowCancel;
   readonly Stopwatch _stopwatch = Stopwatch.StartNew();
   readonly int _depth;
   readonly int _previousNestingDepth;
   readonly IScopePanel? _previousParentScope;
   readonly TaskLogEntry? _previousLogEntry;
   bool _disposed;

   internal IScopePanel? ScopePanel { get; }

   internal TaskLogEntry LogEntry { get; }

   internal TaskRunnerScope(TaskRunner taskRunner, string scopeTitle, bool visible, bool allowCancel, int depth, int previousNestingDepth, IScopePanel? previousParentScope, TaskLogEntry? parentLogEntry)
   {
      _taskRunner = taskRunner;
      _scopeTitle = scopeTitle;
      _allowCancel = allowCancel;
      _visible = visible;
      _depth = depth;
      _previousNestingDepth = previousNestingDepth;
      _previousParentScope = previousParentScope;
      _previousLogEntry = parentLogEntry;
      LogEntry = new TaskLogEntry(scopeTitle);
      parentLogEntry?.AddChild(LogEntry);
      ScopePanel = visible ? taskRunner.CreateScopePanel(scopeTitle, visible, depth) : null;
   }

   ITaskProgressRunner CreateRunner(string message, bool async = false)
   {
      var logMessage = async ? $"(async) {message}" : message;
      var taskLogEntry = new TaskLogEntry(logMessage);
      LogEntry.AddChild(taskLogEntry);
      return new LoggingTaskRunnerWrapper(_taskRunner.Create(ScopePanel, message, _visible, _allowCancel), taskLogEntry);
   }

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
      using var runner = CreateRunner(message, async: true);
      return await runner.RunBatchAsync(items, processItem, message, threadCount);
   }

   public async Task<TResult> RunIndeterminateAsync<TResult>(string message, Func<TResult> action)
   {
      using var runner = CreateRunner(message, async: true);
      return await runner.RunIndeterminateAsync(message, action);
   }

   public void SetLabelText(string text)
   { /* No persistent panel — each method manages its own */
   }

   public bool IsHidden() => !_visible;

   public void Dispose()
   {
      if(_disposed) return;
      _disposed = true;

      _stopwatch.Stop();
      LogEntry.MarkCompleted();

      if(_depth == 1)
      {
         this.Log().Info($"{Environment.NewLine}{LogEntry.FormatTree()}");
      }

      ScopePanel?.Dispose();
      _taskRunner.OnScopeDisposed(_previousNestingDepth, _previousParentScope, _previousLogEntry);
   }
}
