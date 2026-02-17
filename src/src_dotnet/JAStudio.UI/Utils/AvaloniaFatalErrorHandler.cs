using System;
using Avalonia.Threading;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Utils;

class AvaloniaFatalErrorHandler : IFatalErrorHandler
{
   public void Handle(Exception exception) =>
      Dispatcher.UIThread.Post(() => FatalErrorDialog.Show(exception));
}
