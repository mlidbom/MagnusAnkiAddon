using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Compze.Utilities.SystemCE.ActionFuncHarmonization;

namespace JAStudio.Core.TaskRunners;

public interface ITaskProgressRunner : IDisposable
{
   void ProcessWithProgress<TInput>(List<TInput> items, Action<TInput> processItem, string message) => ProcessWithProgress(items, processItem.AsFunc(), message, ThreadCount.One);
   void ProcessWithProgress<TInput>(List<TInput> items, Action<TInput> processItem, string message, ThreadCount threads) => ProcessWithProgress(items, processItem.AsFunc(), message, threads);
   public List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message) => ProcessWithProgress(items, processItem, message, ThreadCount.One);
   List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads);

   Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threadCount);

   Task ProcessWithProgressAsync<TInput>(List<TInput> items, Action<TInput> processItem, string message) => ProcessWithProgressAsync(items, processItem.AsFunc(), message, ThreadCount.One);
   Task ProcessWithProgressAsync<TInput>(List<TInput> items, Action<TInput> processItem, string message, ThreadCount threadCount) => ProcessWithProgressAsync(items, processItem.AsFunc(), message, threadCount);

   TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action);
   Task<TResult> RunOnBackgroundThreadWithSpinningProgressDialogAsync<TResult>(string message, Func<TResult> action);
   Task RunOnBackgroundThreadWithSpinningProgressDialogAsync(string message, Action action) => RunOnBackgroundThreadWithSpinningProgressDialogAsync(message, action.AsFunc());
}
