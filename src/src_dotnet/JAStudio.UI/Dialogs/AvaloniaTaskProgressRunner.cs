using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using Avalonia.Threading;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

class AvaloniaTaskProgressRunner : ITaskProgressRunner
{
   TaskProgressViewModel? _viewModel;
   readonly TaskProgressScopeViewModel _scopeViewModel;
   readonly bool _allowCancel;
   string _labelText;

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
      if(_viewModel != null) throw new InvalidOperationException("Cannot switch from spinner to batch mode within the same runner.");
      var batchVm = new BatchTaskProgressViewModel { Message = _labelText, IsCancelVisible = _allowCancel };
      _viewModel = batchVm;
      Dispatcher.UIThread.Invoke(() => _scopeViewModel.Children.Add(batchVm));
      return batchVm;
   }

   public bool IsHidden() => false;

   public void SetLabelText(string text)
   {
      _labelText = text;
      if(_viewModel != null) _viewModel.Message = text;
   }

   public TResult RunIndeterminate<TResult>(string message, Func<TResult> action)
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

   public async Task<TResult> RunIndeterminateAsync<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);
      var vm = EnsureSpinnerViewModel();
      vm.Message = message;

      return await TaskCE.Run(action);
   }

   public List<TOutput> RunBatch<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads)
   {
      var totalItems = items.Count;
      var results = new TOutput[totalItems];
      using var _ = this.Log().Info().LogMethodExecutionTime($"{message} handled {items.Count} items ({threads.Threads} threads)");

      var vm = EnsureBatchViewModel();
      vm.Message = message;
      vm.SetProgress(0, totalItems);

      var completed = 0;
      var lastRefreshTicks = Stopwatch.GetTimestamp();
      var stopwatch = Stopwatch.StartNew();

      void UpdateProgress()
      {
         var current = System.Threading.Interlocked.Increment(ref completed);
         var nowTicks = Stopwatch.GetTimestamp();
         var lastTicks = System.Threading.Interlocked.Read(ref lastRefreshTicks);
         var elapsedSinceRefresh = (nowTicks - lastTicks) * 1000.0 / Stopwatch.Frequency;

         if(elapsedSinceRefresh > 100 || current == totalItems)
         {
            System.Threading.Interlocked.Exchange(ref lastRefreshTicks, nowTicks);
            vm.UpdateProgressWithTiming(current, totalItems, stopwatch);

            if(Dispatcher.UIThread.CheckAccess())
               Dispatcher.UIThread.RunJobs();
         }
      }

      if(threads.IsSequential)
      {
         for(var i = 0; i < totalItems; i++)
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

      return [..results];
   }

   public async Task<List<TOutput>> RunBatchAsync<TInput, TOutput>(List<TInput> items, Func<TInput, TOutput> processItem, string message, ThreadCount threads) =>
      await TaskCE.Run(() => RunBatch(items, processItem, message, threads));

   public void Close()
   {
      if(_viewModel != null)
         Dispatcher.UIThread.Post(() => _scopeViewModel.Children.Remove(_viewModel));
   }

   public void Dispose() => Close();
}
