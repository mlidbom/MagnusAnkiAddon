using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Avalonia.Threading;
using Compze.Utilities.Logging;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

class AvaloniaTaskProgressRunner : ITaskProgressRunner
{
   TaskProgressPanel _panel = null!;
   readonly bool _allowCancel;

   public AvaloniaTaskProgressRunner(string windowTitle, string labelText, bool allowCancel)
   {
      _allowCancel = allowCancel;
      Dispatcher.UIThread.Invoke(() => _panel = MultiTaskProgressDialog.CreatePanel(windowTitle, labelText, allowCancel));
   }

   public List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads) => Dispatcher.UIThread.Invoke(() =>
   {
      using var _ = this.Log().Info().LogMethodExecutionTime($"{nameof(ProcessWithProgress)}: executed {message}: handling {items.Count} items using ({threads.Threads} threads)");
      InitListProcessingProgress(items, message);
      var task = Task.Run(() => ProcessItems(items, processItem, message, threads));
      KeepUIThreadAliveWhileWaitingForTaskToComplete(task);
      return task.Result;
   });

   public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action) => Dispatcher.UIThread.Invoke(() =>
   {
      using var _ = this.Log().Info().LogMethodExecutionTime($"{nameof(ProcessWithProgress)}{message}: executed {message}");
      SetPanelToProgressSpinnerMode(message);
      return RunActionOnBackgroundThread(message, action);
   });

   public Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime($"{nameof(ProcessWithProgress)}: executed {message}: handling {items.Count} items using ({threads.Threads} threads)");
      Dispatcher.UIThread.Post(() => InitListProcessingProgress(items, message));
      return Task.Run(() => ProcessItems(items, processItem, message, threads));
   }

   public async Task<TResult> RunOnBackgroundThreadWithSpinningProgressDialogAsync<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime($"{nameof(ProcessWithProgress)}{message}: executed {message}");
      Dispatcher.UIThread.Post(() => SetPanelToProgressSpinnerMode(message));
      return await Task.Run(action);
   }

   public void Close() => Dispatcher.UIThread.Post(() => MultiTaskProgressDialog.RemovePanel(_panel));

   public void Dispose() => Close();

   //Private helpers
   static void KeepUIThreadAliveWhileWaitingForTaskToComplete(Task task)
   {
      while(!task.IsCompleted) Dispatcher.UIThread.RunJobs();
   }

   void SetPanelToProgressSpinnerMode(string message)
   {
      _panel.SetMessage(message);
      _panel.SetIndeterminate(true);
   }

   void InitListProcessingProgress<TInput>(List<TInput> items, string message)
   {
      _panel.SetMessage($"{message} 0 of {items.Count}");
      _panel.SetIndeterminate(false);
      _panel.SetProgress(0, items.Count);
   }

   TResult RunActionOnBackgroundThread<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);
      var task = Task.Run(action);
      KeepUIThreadAliveWhileWaitingForTaskToComplete(task);
      return task.Result;
   }

   List<TOutput> ProcessItems<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      var totalItems = items.Count;
      var results = new TOutput[totalItems];
      int completed = 0;
      var startTime = DateTime.Now;
      var lastRefresh = DateTime.Now;

      void UpdateProgress()
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
            UpdateProgress();
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
                         UpdateProgress();
                      });
      }

      return new List<TOutput>(results);
   }

   static string FormatSeconds(double seconds)
   {
      var timeSpan = TimeSpan.FromSeconds(seconds);
      return $"{timeSpan.Hours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2}";
   }
}
