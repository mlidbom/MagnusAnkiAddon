using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Avalonia.Threading;
using Compze.Utilities.Logging;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

public class AvaloniaTaskProgressRunner : ITaskProgressRunner
{
   TaskProgressPanel _panel = null!;
   readonly bool _allowCancel;

   public AvaloniaTaskProgressRunner(string windowTitle, string labelText, bool allowCancel)
   {
      _allowCancel = allowCancel;
      Dispatcher.UIThread.Invoke(() => _panel = MultiTaskProgressDialog.CreatePanel(windowTitle, labelText, allowCancel));
   }

   static void KeepUIThreadAliveWhileWaitingForTaskToComplete(Task task)
   {
      while(!task.IsCompleted) Dispatcher.UIThread.RunJobs();
   }

   public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action) => Dispatcher.UIThread.Invoke(() =>
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);

      _panel.SetMessage(message);
      _panel.SetIndeterminate(true);

      var task = Task.Run(action);

      KeepUIThreadAliveWhileWaitingForTaskToComplete(task);

      return task.Result;
   });

   public async Task<TResult> RunOnBackgroundThreadWithSpinningProgressDialogAsync<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);

      Dispatcher.UIThread.Post(() =>
      {
         _panel.SetMessage(message);
         _panel.SetIndeterminate(true);
      });

      return await Task.Run(action);
   }

   public List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads) => Dispatcher.UIThread.Invoke(() =>
   {
      var totalItems = items.Count;
      var results = new TOutput[totalItems];
      using var _ = this.Log().Info().LogMethodExecutionTime($"{message} handled {items.Count} items ({threads.Threads} threads)");

      _panel.SetMessage($"{message} 0 of {totalItems}");
      _panel.SetIndeterminate(false);
      _panel.SetProgress(0, totalItems);

      int completed = 0;
      var startTime = DateTime.Now;
      var lastRefresh = DateTime.Now;

      void UpdateProgressFromAnyThread()
      {
         var now = DateTime.Now;
         var current = System.Threading.Interlocked.Increment(ref completed);
         if((now - lastRefresh).TotalMilliseconds > 100 || current == totalItems)
         {
            lastRefresh = now;
            var elapsed = current > 0 ? (now - startTime).TotalSeconds : 0;
            var estimatedTotal = current > 0 ? (elapsed / current) * totalItems : 0;
            var estimatedRemaining = current > 0 ? estimatedTotal - elapsed : 0;
            var progressMessage = current > 0
                                     ? $"{message} {current} of {totalItems} Total: {FormatSeconds(estimatedTotal)} Elapsed: {FormatSeconds(elapsed)} Remaining: {FormatSeconds(estimatedRemaining)}"
                                     : $"{message} {current} of {totalItems}";

            var capturedCurrent = current;
            var capturedMsg = progressMessage;
            Dispatcher.UIThread.Post(() =>
            {
               _panel.SetProgress(capturedCurrent, totalItems);
               _panel.SetMessage(capturedMsg);
            });
         }
      }

      if(threads.IsSequential)
      {
         for(int i = 0; i < totalItems; i++)
         {
            if(_allowCancel && _panel.WasCanceled)
            {
               JALogger.Log($"Operation canceled by user after {completed} of {totalItems} items");
               break;
            }

            results[i] = processItem(items[i]);
            UpdateProgressFromAnyThread();
            Dispatcher.UIThread.RunJobs();
         }
      } else
      {
         Parallel.For(0,
                      totalItems,
                      threads.ParallelOptions,
                      i =>
                      {
                         if(_allowCancel && _panel.WasCanceled) return;
                         results[i] = processItem(items[i]);
                         UpdateProgressFromAnyThread();
                      });
      }

      return new List<TOutput>(results);
   });

   public Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      var totalItems = items.Count;
      using var _ = this.Log().Info().LogMethodExecutionTime($"{message} handled {items.Count} items ({threads.Threads} threads)");

      Dispatcher.UIThread.Post(() =>
      {
         _panel.SetMessage($"{message} 0 of {totalItems}");
         _panel.SetIndeterminate(false);
         _panel.SetProgress(0, totalItems);
      });

      return Task.Run(() =>
      {
         var results = new TOutput[totalItems];
         int completed = 0;
         var startTime = DateTime.Now;
         var lastRefresh = DateTime.Now;

         void UpdateProgress(int justCompleted)
         {
            var now = DateTime.Now;
            var current = System.Threading.Interlocked.Add(ref completed, justCompleted);
            if((now - lastRefresh).TotalMilliseconds > 100 || current == totalItems)
            {
               lastRefresh = now;
               var elapsed = current > 0 ? (now - startTime).TotalSeconds : 0;
               var estimatedTotal = current > 0 ? (elapsed / current) * totalItems : 0;
               var estimatedRemaining = current > 0 ? estimatedTotal - elapsed : 0;
               var progressMessage = current > 0
                                        ? $"{message} {current} of {totalItems} Total: {FormatSeconds(estimatedTotal)} Elapsed: {FormatSeconds(elapsed)} Remaining: {FormatSeconds(estimatedRemaining)}"
                                        : $"{message} {current} of {totalItems}";

               var capturedCurrent = current;
               var capturedMsg = progressMessage;
               Dispatcher.UIThread.Post(() =>
               {
                  _panel.SetProgress(capturedCurrent, totalItems);
                  _panel.SetMessage(capturedMsg);
               });
            }
         }

         if(threads.IsSequential)
         {
            for(int i = 0; i < totalItems; i++)
            {
               if(_allowCancel && _panel.WasCanceled)
               {
                  JALogger.Log($"Operation canceled by user after {completed} of {totalItems} items");
                  break;
               }

               results[i] = processItem(items[i]);
               UpdateProgress(1);
            }
         } else
         {
            Parallel.For(0,
                         totalItems,
                         threads.ParallelOptions,
                         i =>
                         {
                            if(_allowCancel && _panel.WasCanceled) return;
                            results[i] = processItem(items[i]);
                            UpdateProgress(1);
                         });
         }

         return new List<TOutput>(results);
      });
   }

   static string FormatSeconds(double seconds)
   {
      var timeSpan = TimeSpan.FromSeconds(seconds);
      return $"{timeSpan.Hours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2}";
   }

   public void Close() => Dispatcher.UIThread.Post(() => MultiTaskProgressDialog.RemovePanel(_panel));

   public void Dispose() => Close();
}
