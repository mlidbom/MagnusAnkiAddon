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
   TaskProgressViewModel? _viewModel;
   readonly TaskProgressScopeViewModel _scopeViewModel;
   readonly bool _allowCancel;
   readonly string _labelText;

   public AvaloniaTaskProgressRunner(TaskProgressScopeViewModel scopeViewModel, string labelText, bool allowCancel)
   {
      _scopeViewModel = scopeViewModel;
      _allowCancel = allowCancel;
      _labelText = labelText;
   }

   TaskProgressViewModel EnsureSpinnerViewModel()
   {
      if(_viewModel != null) return _viewModel;
      _viewModel = new TaskProgressViewModel { Message = _labelText, IsCancelVisible = _allowCancel };
      Dispatcher.UIThread.Invoke(() => _scopeViewModel.Children.Add(_viewModel));
      return _viewModel;
   }

   BatchTaskProgressViewModel EnsureBatchViewModel()
   {
      if(_viewModel is BatchTaskProgressViewModel batch) return batch;
      if(_viewModel != null) throw new System.InvalidOperationException("Cannot switch from spinner to batch mode within the same runner.");
      var batchVm = new BatchTaskProgressViewModel { Message = _labelText, IsCancelVisible = _allowCancel };
      _viewModel = batchVm;
      Dispatcher.UIThread.Invoke(() => _scopeViewModel.Children.Add(batchVm));
      return batchVm;
   }

   public bool IsHidden() => false;

   public void SetLabelText(string text)
   {
      if(_viewModel != null) _viewModel.Message = text;
   }

   public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);
      var vm = EnsureSpinnerViewModel();
      vm.Message = message;

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
      var vm = EnsureSpinnerViewModel();
      vm.Message = message;

      return await TaskCE.Run(action);
   }

   public List<TOutput> ProcessWithProgress<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      var totalItems = items.Count;
      var results = new TOutput[totalItems];
      using var _ = this.Log().Info().LogMethodExecutionTime($"{message} handled {items.Count} items ({threads.Threads} threads)");

      var vm = EnsureBatchViewModel();
      vm.Message = message;
      vm.SetProgress(0, totalItems);

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
            vm.UpdateProgressWithTiming(current, totalItems, startTime);

            if(Dispatcher.UIThread.CheckAccess())
               Dispatcher.UIThread.RunJobs();
         }
      }

      if(threads.IsSequential)
      {
         for(int i = 0; i < totalItems; i++)
         {
            if(_allowCancel && vm.WasCanceled)
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
                         if(_allowCancel && vm.WasCanceled) return;
                         results[i] = processItem(items[i]);
                         UpdateProgress();
                      });
      }

      return new List<TOutput>(results);
   }

   public async Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      var totalItems = items.Count;
      var vm = EnsureBatchViewModel();
      vm.Message = message;
      vm.SetProgress(0, totalItems);

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
               vm.UpdateProgressWithTiming(current, totalItems, startTime);
            }
         }

         if(threads.IsSequential)
         {
            for(int i = 0; i < totalItems; i++)
            {
               if(_allowCancel && vm.WasCanceled)
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
                            if(_allowCancel && vm.WasCanceled) return;
                            results[i] = processItem(items[i]);
                            UpdateProgress(1);
                         });
         }

         return new List<TOutput>(results);
      });
   }

   public void Close()
   {
      if(_viewModel != null)
         Dispatcher.UIThread.Post(() => _scopeViewModel.Children.Remove(_viewModel));
   }

   public void Dispose() => Close();
}
