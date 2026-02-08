using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Compze.Utilities.SystemCE.ActionFuncHarmonization;

namespace JAStudio.Core.TaskRunners;

public interface ITaskProgressRunner : IDisposable
{
   public List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message) => ProcessWithProgress(items, processItem, message, ThreadCount.One);
   List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads);

   TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action);

   /// <summary>
   /// Async version of <see cref="ProcessWithProgress{TInput,TOutput}"/>.
   /// Runs processing on a background thread while posting progress updates to the UI.
   /// Multiple async operations can run in parallel, each with its own progress display.
   /// Use <paramref name="threadCount"/> to process items concurrently within this operation.
   /// </summary>
   Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threadCount);

   Task ProcessWithProgressAsync<TInput>(List<TInput> items, Action<TInput> processItem, string message) => ProcessWithProgressAsync(items, processItem.AsFunc(), message, ThreadCount.One);
   Task ProcessWithProgressAsync<TInput>(List<TInput> items, Action<TInput> processItem, string message, ThreadCount threadCount) => ProcessWithProgressAsync(items, processItem.AsFunc(), message, threadCount);

   /// <summary>
   /// Async version of <see cref="RunOnBackgroundThreadWithSpinningProgressDialog{TResult}"/>.
   /// Runs the action on a background thread with an indeterminate progress indicator.
   /// </summary>
   Task<TResult> RunOnBackgroundThreadWithSpinningProgressDialogAsync<TResult>(string message, Func<TResult> action);

   Task RunOnBackgroundThreadAsync(string message, Action action) => RunOnBackgroundThreadWithSpinningProgressDialogAsync(message, action.AsFunc());
}
