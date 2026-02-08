using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;

namespace JAStudio.Core.TaskRunners;

public class InvisibleTaskRunner : ITaskProgressRunner
{
   public InvisibleTaskRunner(string windowTitle, string labelText)
   {
      MyLog.Debug($"##--InvisibleTaskRunner--## Created for {windowTitle} - {labelText}");
   }

   public List<TOutput> ProcessWithProgress<TInput, TOutput>(
      List<TInput> items,
      Func<TInput, TOutput> processItem,
      string message)
   {
      var watch = Stopwatch.StartNew();
      var result = new List<TOutput>();
      foreach(var item in items)
      {
         result.Add(processItem(item));
      }

      var totalItems = items.Count;
      watch.Stop();
      MyLog.Debug($"##--InvisibleTaskRunner--## Finished {message} in {watch.Elapsed:g} handled {totalItems} items");

      return result;
   }

   public Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(
      List<TInput> items,
      Func<TInput, TOutput> processItem,
      string message,
      Parallelism? parallelism = null)
   {
      var threads = (parallelism ?? Parallelism.Sequential).Threads;
      return Task.Run(() =>
      {
         if(threads <= 1)
            return ProcessWithProgress(items, processItem, message);

         var watch = Stopwatch.StartNew();
         var results = new TOutput[items.Count];
         System.Threading.Tasks.Parallel.For(0, items.Count,
            new System.Threading.Tasks.ParallelOptions { MaxDegreeOfParallelism = threads },
            i => results[i] = processItem(items[i]));
         watch.Stop();
         MyLog.Debug($"##--InvisibleTaskRunner--## Finished {message} in {watch.Elapsed:g} handled {items.Count} items ({threads} threads)");
         return new List<TOutput>(results);
      });
   }

   public void SetLabelText(string labelText)
   {
      // Invisible - no-op
   }

   public void RunGc()
   {
      // No-op for invisible runner
   }

   public void Close()
   {
      // Invisible - no-op
   }

   public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action)
   {
      var watch = Stopwatch.StartNew();
      var result = action();
      watch.Stop();
      MyLog.Debug($"##--InvisibleTaskRunner--## Finished {message} in {watch.Elapsed:g}");
      return result;
   }

   public Task<TResult> RunOnBackgroundThreadAsync<TResult>(string message, Func<TResult> action)
   {
      return Task.Run(() => RunOnBackgroundThreadWithSpinningProgressDialog(message, action));
   }

   public bool IsHidden()
   {
      return true;
   }

   public void Dispose()
   {
      Close();
   }
}
