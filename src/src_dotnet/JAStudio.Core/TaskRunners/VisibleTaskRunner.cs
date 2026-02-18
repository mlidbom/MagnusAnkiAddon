using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Task progress runner that updates a <see cref="TaskProgressScopeViewModel"/>'s children
/// with live progress information. Uses <see cref="IUIThreadDispatcher"/> for thread-safe
/// access to the view model's <c>Children</c> collection.
/// </summary>
class VisibleTaskRunner(TaskProgressScopeViewModel scopeViewModel, IUIThreadDispatcher dispatcher, string labelText, bool allowCancel) : ITaskProgressRunner
{
   TaskProgressViewModel? _viewModel;
   readonly TaskProgressScopeViewModel _scopeViewModel = scopeViewModel;
   readonly IUIThreadDispatcher _dispatcher = dispatcher;
   readonly bool _allowCancel = allowCancel;
   string _labelText = labelText;

   TaskProgressViewModel EnsureSpinnerViewModel()
   {
      if(_viewModel != null) return _viewModel;
      _viewModel = new TaskProgressViewModel { Message = _labelText, IsCancelVisible = _allowCancel };
      _dispatcher.InvokeSynchronouslyOnUIThread(() => _scopeViewModel.Children.Add(_viewModel));
      return _viewModel;
   }

   BatchTaskProgressViewModel EnsureBatchViewModel()
   {
      if(_viewModel is BatchTaskProgressViewModel batchViewModel) return batchViewModel;
      if(_viewModel != null) throw new InvalidOperationException("Cannot switch from spinner to batch mode within the same runner.");
      var batchVm = new BatchTaskProgressViewModel { Message = _labelText, IsCancelVisible = _allowCancel };
      _viewModel = batchVm;
      _dispatcher.InvokeSynchronouslyOnUIThread(() => _scopeViewModel.Children.Add(batchVm));
      return batchVm;
   }

   public TResult RunIndeterminate<TResult>(string message, Func<TResult> action)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime(message);
      var vm = EnsureSpinnerViewModel();
      vm.Message = message;

      var task = TaskCE.Run(action);

      // Wait for completion, processing UI events to keep the dialog responsive
      while(!task.IsCompleted)
      {
         if(_dispatcher.CurrentThreadIsUIThread())
            _dispatcher.PumpEventsToKeepUIResponsive();
         else
            Thread.Sleep(50);
      }

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
         var current = Interlocked.Increment(ref completed);
         var nowTicks = Stopwatch.GetTimestamp();
         var lastTicks = Interlocked.Read(ref lastRefreshTicks);
         var elapsedSinceRefresh = (nowTicks - lastTicks) * 1000.0 / Stopwatch.Frequency;

         if(elapsedSinceRefresh > 100 || current == totalItems)
         {
            Interlocked.Exchange(ref lastRefreshTicks, nowTicks);
            vm.UpdateProgressWithTiming(current, totalItems, stopwatch);

            if(_dispatcher.CurrentThreadIsUIThread())
               _dispatcher.PumpEventsToKeepUIResponsive();
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

   public void Dispose()
   {
      if(_viewModel != null)
         _dispatcher.PostToUIThread(() => _scopeViewModel.Children.Remove(_viewModel));
   }
}
