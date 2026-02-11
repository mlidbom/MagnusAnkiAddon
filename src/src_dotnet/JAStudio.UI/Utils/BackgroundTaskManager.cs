using System;
using System.Threading.Tasks;
using Avalonia.Threading;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;

namespace JAStudio.UI.Utils;

/// <summary>
/// Fire-and-forget background task runner with crash-safety.
/// Executes an action on a background thread. If the action throws,
/// the exception is logged and a fatal error dialog is shown telling
/// the user to restart.
/// </summary>
public static class BackgroundTaskManager
{
   static readonly ILogger Log = CompzeLogger.For(typeof(BackgroundTaskManager));

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
      Dispatcher.UIThread.Post(() => FatalErrorDialog.Show(ex));
   }
}
