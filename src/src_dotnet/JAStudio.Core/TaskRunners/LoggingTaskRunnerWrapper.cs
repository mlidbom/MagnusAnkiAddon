using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Wraps an <see cref="ITaskProgressRunner"/> to record elapsed time
/// into a <see cref="TaskLogEntry"/> when the operation completes.
/// </summary>
class LoggingTaskRunnerWrapper : ITaskProgressRunner
{
   readonly ITaskProgressRunner _inner;
   readonly TaskLogEntry _logEntry;

   public LoggingTaskRunnerWrapper(ITaskProgressRunner inner, TaskLogEntry logEntry)
   {
      _inner = inner;
      _logEntry = logEntry;
   }

   public List<TOutput> RunBatch<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads) =>
      _inner.RunBatch(items, processItem, message, threads);

   public Task<List<TOutput>> RunBatchAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threadCount) =>
      _inner.RunBatchAsync(items, processItem, message, threadCount);

   public TResult RunIndeterminate<TResult>(string message, Func<TResult> action) =>
      _inner.RunIndeterminate(message, action);

   public Task<TResult> RunIndeterminateAsync<TResult>(string message, Func<TResult> action) =>
      _inner.RunIndeterminateAsync(message, action);

   public void SetLabelText(string text) => _inner.SetLabelText(text);

   public bool IsHidden() => _inner.IsHidden();

   public void Dispose()
   {
      _inner.Dispose();
      _logEntry.MarkCompleted();
   }
}
