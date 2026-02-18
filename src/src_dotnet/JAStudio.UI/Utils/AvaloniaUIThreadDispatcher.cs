using System;
using Avalonia.Threading;
using JAStudio.Core.TaskRunners;
using JAStudio.UI.Dialogs;

namespace JAStudio.UI.Utils;

/// <summary>
/// Avalonia implementation of <see cref="IUIThreadDispatcher"/>.
/// Delegates to <see cref="Dispatcher.UIThread"/> for all thread marshaling.
/// Connects the <see cref="MultiTaskProgressDialog"/> to the
/// <see cref="TaskProgressDialogViewModel"/> for dialog lifecycle management.
/// </summary>
class AvaloniaUIThreadDispatcher : IUIThreadDispatcher
{
   public void PostToUIThread(Action action) => Dispatcher.UIThread.Post(action);
   public void InvokeSynchronouslyOnUIThread(Action action) => Dispatcher.UIThread.Invoke(action);
   public bool CurrentThreadIsUIThread() => Dispatcher.UIThread.CheckAccess();
   public void PumpEventsToKeepUIResponsive() => Dispatcher.UIThread.RunJobs();

   public void OnTaskRunnerInstantiated(TaskProgressDialogViewModel viewModel)
   {
      viewModel.PropertyChanged += (_, e) =>
      {
         if(e.PropertyName != nameof(TaskProgressDialogViewModel.IsVisible)) return;

         // PropertyChanged fires on the UI thread (TaskRunner uses IUIThreadDispatcher),
         // so we can safely manage the dialog window here.
         if(viewModel.IsVisible)
            MultiTaskProgressDialog.Show(viewModel);
         else
            MultiTaskProgressDialog.Hide();
      };
   }
}
