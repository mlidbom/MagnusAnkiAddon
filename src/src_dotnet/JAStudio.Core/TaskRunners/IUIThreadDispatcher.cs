using System;

namespace JAStudio.Core.TaskRunners;

/// <summary>Abstraction for dispatching work to the UI thread, if there is one.</summary>
public interface IUIThreadDispatcher
{
   void PostToUIThread(Action action);
   void InvokeSynchronouslyOnUIThread(Action action);
   bool CurrentThreadIsUIThread();
   void PumpEventsToKeepUIResponsive();

   /// <summary> Called once during when a task runner is instantiated to enable whatever initialization might be needed.</summary>
   void OnTaskRunnerInstantiated(TaskProgressDialogViewModel viewModel);
}
