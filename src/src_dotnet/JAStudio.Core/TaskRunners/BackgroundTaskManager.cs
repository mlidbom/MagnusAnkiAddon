using System;
using System.Threading.Tasks;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Fire-and-forget background task runner with crash-safety.
/// Executes an action on a background thread. If the action throws,
/// the exception is logged and the registered fatal error handler is invoked.
/// </summary>
public class BackgroundTaskManager
{
   static readonly ILogger Log = CompzeLogger.For(typeof(BackgroundTaskManager));
   readonly IFatalErrorHandler _fatalErrorHandler;

   internal BackgroundTaskManager(IFatalErrorHandler fatalErrorHandler) => _fatalErrorHandler = fatalErrorHandler;

   /// <summary>
   /// Run a synchronous action on a background thread with error handling.
   /// </summary>
   public void Run(Action action)
   {
      TaskCE.Run(() =>
      {
         try
         {
            action();
         }
         catch(Exception ex)
         {
            HandleException(ex);
         }
      });
   }

   /// <summary>
   /// Run an async action on a background thread with error handling.
   /// TaskCanceledException is silently ignored (expected for debounced/cancelled work).
   /// </summary>
   public void RunAsync(Func<Task> action)
   {
      TaskCE.Run(async () =>
      {
         try
         {
            await action();
         }
         catch(OperationCanceledException)
         {
            // Expected for debounced/cancelled work — not an error.
         }
         catch(Exception ex)
         {
            HandleException(ex);
         }
      });
   }

   void HandleException(Exception ex)
   {
      Log.Error(ex, "Unhandled exception in background task:");
      _fatalErrorHandler.Handle(ex);
   }
}
