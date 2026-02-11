using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;

namespace JAStudio.Core.TaskRunners;

public class InvisibleTaskRunner : ITaskProgressRunner
{
   public InvisibleTaskRunner(string labelText)
   {
      this.Log().Debug($"##--InvisibleTaskRunner--## Created for {labelText}");
   }

   public List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      var watch = Stopwatch.StartNew();

      if(threads.IsSequential)
      {
         var result = new List<TOutput>(items.Count);
         foreach(var item in items)
         {
            result.Add(processItem(item));
         }

         watch.Stop();
         this.Log().Debug($"##--InvisibleTaskRunner--## Finished {message} in {watch.Elapsed:g} handled {items.Count} items");
         return result;
      } else
      {
         var results = new TOutput[items.Count];
         Parallel.For(0,
                      items.Count,
                      threads.ParallelOptions,
                      i => results[i] = processItem(items[i]));
         watch.Stop();
         this.Log().Debug($"##--InvisibleTaskRunner--## Finished {message} in {watch.Elapsed:g} handled {items.Count} items ({threads.Threads} threads)");
         return new List<TOutput>(results);
      }
   }

   public Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads) =>
      TaskCE.Run(() => ProcessWithProgress(items, processItem, message, threads));

   public void SetLabelText(string labelText) { }

   public void Close() { }

   public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action)
   {
      var watch = Stopwatch.StartNew();
      var result = action();
      watch.Stop();
      this.Log().Debug($"##--InvisibleTaskRunner--## Finished {message} in {watch.Elapsed:g}");
      return result;
   }

   public Task<TResult> RunOnBackgroundThreadWithSpinningProgressDialogAsync<TResult>(string message, Func<TResult> action) =>
      TaskCE.Run(() => RunOnBackgroundThreadWithSpinningProgressDialog(message, action));

   public bool IsHidden() => true;

   public void Dispose() { }
}
