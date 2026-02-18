using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Manages the lifecycle of progress view models within a parent scope.
/// Handles adding/removing child VMs from the scope's <c>Children</c> collection,
/// UI thread dispatch, event pumping, and throttled batch progress updates.
/// <see cref="VisibleTaskRunner"/> delegates all presentation concerns here.
/// </summary>
class ScopeProgressPresenter : IDisposable
{
   readonly TaskProgressScopeViewModel _scopeViewModel;
   readonly IUIThreadDispatcher _dispatcher;
   readonly bool _allowCancel;
   TaskProgressViewModel? _viewModel;
   long _lastRefreshTicks;

   internal ScopeProgressPresenter(TaskProgressScopeViewModel scopeViewModel, IUIThreadDispatcher dispatcher, bool allowCancel)
   {
      _scopeViewModel = scopeViewModel;
      _dispatcher = dispatcher;
      _allowCancel = allowCancel;
   }

   internal TaskProgressViewModel ShowSpinnerForTaskNamed(string message)
   {
      if(_viewModel != null)
      {
         _viewModel.Message = message;
         return _viewModel;
      }

      _viewModel = new TaskProgressViewModel { Message = message, IsCancelVisible = _allowCancel };
      _dispatcher.InvokeSynchronouslyOnUIThread(() => _scopeViewModel.Children.Add(_viewModel));
      return _viewModel;
   }

   internal BatchTaskProgressViewModel ShowBatchProgress(string message, int total)
   {
      if(_viewModel is BatchTaskProgressViewModel existing)
      {
         existing.Message = message;
         existing.SetProgress(0, total);
         return existing;
      }

      if(_viewModel != null) throw new InvalidOperationException("Cannot switch from spinner to batch mode within the same runner.");

      var batchViewModel = new BatchTaskProgressViewModel { Message = message, IsCancelVisible = _allowCancel };
      batchViewModel.SetProgress(0, total);
      _viewModel = batchViewModel;
      _dispatcher.InvokeSynchronouslyOnUIThread(() => _scopeViewModel.Children.Add(batchViewModel));
      _lastRefreshTicks = Stopwatch.GetTimestamp();
      return batchViewModel;
   }

   /// <summary>Updates batch progress with throttled timing updates (max every 100ms). Thread-safe: called from parallel worker threads during batch processing. Pumps UI events when called from the UI thread to keep the dialog responsive.</summary>
   internal void UpdateBatchProgressDisplay(int current, int total, Stopwatch stopwatch)
   {
      var nowTicks = Stopwatch.GetTimestamp();
      var lastTicks = Interlocked.Read(ref _lastRefreshTicks);
      var elapsedSinceRefresh = (nowTicks - lastTicks) * 1000.0 / Stopwatch.Frequency;

      if(elapsedSinceRefresh > 100 || current == total)
      {
         Interlocked.Exchange(ref _lastRefreshTicks, nowTicks);
         ((BatchTaskProgressViewModel)_viewModel!).UpdateProgressWithTiming(current, total, stopwatch);

         if(_dispatcher.CurrentThreadIsUIThread())
            _dispatcher.PumpEventsToKeepUIResponsive();
      }
   }

   /// <summary> Blocks until the task completes, pumping UI events if on the UI thread to keep the dialog responsive during synchronous waits. </summary>
   internal void KeepUIResponsiveUntilTaskIsDone(Task task)
   {
      while(!task.IsCompleted)
      {
         if(_dispatcher.CurrentThreadIsUIThread())
            _dispatcher.PumpEventsToKeepUIResponsive();
         else
            Thread.Sleep(50);
      }
   }

   public void Dispose()
   {
      if(_viewModel != null)
         _dispatcher.PostToUIThread(() => _scopeViewModel.Children.Remove(_viewModel));
   }
}
