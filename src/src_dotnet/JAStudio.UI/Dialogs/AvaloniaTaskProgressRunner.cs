using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using Avalonia.Threading;
using Compze.Utilities.Logging;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

public class AvaloniaTaskProgressRunner : ITaskProgressRunner
{
   TaskProgressPanel _panel = null!;
   readonly bool _allowCancel;
   readonly Stopwatch _stopwatch = Stopwatch.StartNew();

   public AvaloniaTaskProgressRunner(string windowTitle, string labelText, bool allowCancel, bool modal)
   {
      _allowCancel = allowCancel;

      // All Avalonia control creation and interaction must happen on the UI thread.
      // Marshal here so callers never need to know about Avalonia threading.
      Dispatcher.UIThread.Invoke(() =>
      {
         _panel = MultiTaskProgressDialog.CreatePanel(windowTitle, labelText, allowCancel);
      });
   }

   public bool IsHidden() => false;

   public void SetLabelText(string text) => Dispatcher.UIThread.Post(() => _panel.SetMessage(text));

   public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);
      Dispatcher.UIThread.Invoke(() =>
      {
         _panel.SetMessage(message);
         _panel.SetIndeterminate(true);
      });

      var task = Task.Run(action);

      // Wait for completion, processing UI events
      while(!task.IsCompleted)
      {
         if(Dispatcher.UIThread.CheckAccess())
            Dispatcher.UIThread.RunJobs();
         else
            System.Threading.Thread.Sleep(50);
      }

      if(task.IsFaulted) throw task.Exception!.InnerException!;

      return task.Result;
   }

   public async Task<TResult> RunOnBackgroundThreadAsync<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);

      Dispatcher.UIThread.Post(() =>
      {
         _panel.SetMessage(message);
         _panel.SetIndeterminate(true);
      });

      return await Task.Run(action);
   }

   public List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message)
   {
      var totalItems = items.Count;
      var results = new List<TOutput>(totalItems);
      using var _ = this.Log().Info().LogMethodExecutionTime($"{message} handled {items.Count} items");

      Dispatcher.UIThread.Invoke(() =>
      {
         _panel.SetMessage($"{message} 0 of {totalItems}");
         _panel.SetIndeterminate(false);
         _panel.SetProgress(0, totalItems);
      });

      var startTime = DateTime.Now;
      var lastRefresh = DateTime.Now;

      for(int i = 0; i < totalItems; i++)
      {
         // Check for cancellation
         if(_allowCancel && _panel.WasCanceled)
         {
            JALogger.Log($"Operation canceled by user after {i} of {totalItems} items");
            break;
         }

         // Process item
         results.Add(processItem(items[i]));

         // Update UI periodically (every 100ms or on last item)
         var now = DateTime.Now;
         if((now - lastRefresh).TotalMilliseconds > 100 || i == totalItems - 1)
         {
            lastRefresh = now;
            var progressIndex = i + 1;
            var elapsedForEstimate = i > 0 ? (now - startTime).TotalSeconds : 0;
            var estimatedTotal = i > 0 ? (elapsedForEstimate / progressIndex) * totalItems : 0;
            var estimatedRemaining = i > 0 ? estimatedTotal - elapsedForEstimate : 0;
            var progressMessage = i > 0
                                     ? $"{message} {progressIndex} of {totalItems} Total: {FormatSeconds(estimatedTotal)} Elapsed: {FormatSeconds(elapsedForEstimate)} Remaining: {FormatSeconds(estimatedRemaining)}"
                                     : $"{message} {progressIndex} of {totalItems}";

            if(Dispatcher.UIThread.CheckAccess())
            {
               _panel.SetProgress(progressIndex, totalItems);
               _panel.SetMessage(progressMessage);
               Dispatcher.UIThread.RunJobs();
            } else
            {
               Dispatcher.UIThread.Post(() =>
               {
                  _panel.SetProgress(progressIndex, totalItems);
                  _panel.SetMessage(progressMessage);
               });
            }
         }
      }

      return results;
   }

   public Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message)
   {
      var totalItems = items.Count;
      using var _ = this.Log().Info().LogMethodExecutionTime($"{message} handled {items.Count} items");

      Dispatcher.UIThread.Post(() =>
      {
         _panel.SetMessage($"{message} 0 of {totalItems}");
         _panel.SetIndeterminate(false);
         _panel.SetProgress(0, totalItems);
      });

      return Task.Run(() =>
      {
         var results = new List<TOutput>(totalItems);
         var startTime = DateTime.Now;
         var lastRefresh = DateTime.Now;

         for(int i = 0; i < totalItems; i++)
         {
            if(_allowCancel && _panel.WasCanceled)
            {
               JALogger.Log($"Operation canceled by user after {i} of {totalItems} items");
               break;
            }

            results.Add(processItem(items[i]));

            var now = DateTime.Now;
            if((now - lastRefresh).TotalMilliseconds > 100 || i == totalItems - 1)
            {
               lastRefresh = now;
               var progressIndex = i + 1;
               var elapsed = i > 0 ? (now - startTime).TotalSeconds : 0;
               var estimatedTotal = i > 0 ? (elapsed / progressIndex) * totalItems : 0;
               var estimatedRemaining = i > 0 ? estimatedTotal - elapsed : 0;
               var progressMessage = i > 0
                                        ? $"{message} {progressIndex} of {totalItems} Total: {FormatSeconds(estimatedTotal)} Elapsed: {FormatSeconds(elapsed)} Remaining: {FormatSeconds(estimatedRemaining)}"
                                        : $"{message} {progressIndex} of {totalItems}";

               var capturedIdx = progressIndex;
               var capturedMsg = progressMessage;
               Dispatcher.UIThread.Post(() =>
               {
                  _panel.SetProgress(capturedIdx, totalItems);
                  _panel.SetMessage(capturedMsg);
               });
            }
         }

         return results;
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
