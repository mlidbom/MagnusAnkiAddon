using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Avalonia.Threading;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

public class AvaloniaTaskProgressRunner : ITaskProgressRunner
{
   readonly TaskProgressViewModel _viewModel;
   readonly TaskProgressScopeViewModel _scopeViewModel;
   readonly bool _allowCancel;

   public AvaloniaTaskProgressRunner(TaskProgressScopeViewModel scopeViewModel, string labelText, bool allowCancel)
   {
      _scopeViewModel = scopeViewModel;
      _allowCancel = allowCancel;
      _viewModel = new TaskProgressViewModel { Message = labelText, IsCancelVisible = allowCancel };
      Dispatcher.UIThread.Invoke(() => _scopeViewModel.Children.Add(_viewModel));
   }  

   public bool IsHidden() => false;

   public void SetLabelText(string text) => _viewModel.Message = text;

   public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);
      _viewModel.Message = message;
      _viewModel.IsIndeterminate = true;

      var task = TaskCE.Run(action);

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

   public async Task<TResult> RunOnBackgroundThreadWithSpinningProgressDialogAsync<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);
      _viewModel.Message = message;
      _viewModel.IsIndeterminate = true;

      return await TaskCE.Run(action);
   }

   public List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      var totalItems = items.Count;
      var results = new TOutput[totalItems];
      using var _ = this.Log().Info().LogMethodExecutionTime($"{message} handled {items.Count} items ({threads.Threads} threads)");

      _viewModel.Message = message;
      _viewModel.SetProgress(0, totalItems);

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
            _viewModel.UpdateProgressWithTiming(current, totalItems, startTime);

            if(Dispatcher.UIThread.CheckAccess())
               Dispatcher.UIThread.RunJobs();
         }
      }

      if(threads.IsSequential)
      {
         for(int i = 0; i < totalItems; i++)
         {
            if(_allowCancel && _viewModel.WasCanceled)
            {
               this.Log().Info($"Operation canceled by user after {completed} of {totalItems} items");
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
                         if(_allowCancel && _viewModel.WasCanceled) return;
                         results[i] = processItem(items[i]);
                         UpdateProgress();
                      });
      }

      return new List<TOutput>(results);
   }

   public async Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      var totalItems = items.Count;
      _viewModel.Message = message;
      _viewModel.SetProgress(0, totalItems);

      return await TaskCE.Run(() =>
      {
         using var _ = this.Log().Info().LogMethodExecutionTime($"{message} handled {items.Count} items ({threads.Threads} threads)");
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
               _viewModel.UpdateProgressWithTiming(current, totalItems, startTime);
            }
         }

         if(threads.IsSequential)
         {
            for(int i = 0; i < totalItems; i++)
            {
               if(_allowCancel && _viewModel.WasCanceled)
               {
                  this.Log().Info($"Operation canceled by user after {completed} of {totalItems} items");
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
                            if(_allowCancel && _viewModel.WasCanceled) return;
                            results[i] = processItem(items[i]);
                            UpdateProgress(1);
                         });
         }

         return new List<TOutput>(results);
      });
   }

   public void Close() => Dispatcher.UIThread.Post(() => _scopeViewModel.Children.Remove(_viewModel));

   public void Dispose() => Close();
}
