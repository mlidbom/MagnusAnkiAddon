using System;
using System.Threading.Tasks;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Fire-and-forget background task runner with crash-safety.
/// Executes an action on a background thread. If the action throws,
/// the exception is logged and the registered fatal error handler is invoked.
/// Call <see cref="SetFatalErrorHandler"/> at startup to display errors in the UI.
/// </summary>
public static class BackgroundTaskManager
{
   static readonly ILogger Log = CompzeLogger.For(typeof(BackgroundTaskManager));
   static Action<Exception>? _fatalErrorHandler;

   /// <summary>
   /// Register the handler that displays fatal background errors to the user.
   /// Must be called once at startup before any background tasks are fired.
   /// </summary>
   public static void SetFatalErrorHandler(Action<Exception> handler)
   {
      if(_fatalErrorHandler != null) throw new InvalidOperationException("Fatal error handler already set.");
      _fatalErrorHandler = handler;
   }

   /// <summary>
   /// Run a synchronous action on a background thread with error handling.
   /// </summary>
   public static void Run(Action action)
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
   public static void RunAsync(Func<Task> action)
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

   static void HandleException(Exception ex)
   {
      Log.Error(ex, "Unhandled exception in background task:");
      if(_fatalErrorHandler != null)
         _fatalErrorHandler(ex);
      else
         throw new InvalidOperationException("Background task failed and no fatal error handler is registered.", ex);
   }
}
