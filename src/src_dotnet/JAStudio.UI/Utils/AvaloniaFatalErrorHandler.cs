using System;
using Avalonia.Threading;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Utils;

public class AvaloniaFatalErrorHandler : IFatalErrorHandler
{
   public void Handle(Exception exception) =>
      Dispatcher.UIThread.Post(() => FatalErrorDialog.Show(exception));
}
