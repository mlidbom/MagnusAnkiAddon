using Avalonia.Threading;

namespace JAStudio.UI.Utils;

/// <summary>
/// UI-layer setup for <see cref="Core.TaskRunners.BackgroundTaskManager"/>.
/// Wires the Avalonia fatal error dialog as the error handler.
/// After calling <see cref="Initialize"/>, all code should use
/// <see cref="Core.TaskRunners.BackgroundTaskManager"/> directly.
/// </summary>
static class BackgroundTaskManagerSetup
{
   public static void Initialize()
   {
      Core.TaskRunners.BackgroundTaskManager.SetFatalErrorHandler(ex => Dispatcher.UIThread.Post(() => FatalErrorDialog.Show(ex)));
   }
}
