using System;

namespace JAStudio.Core.TaskRunners;

class RethrowingFatalErrorHandler : IFatalErrorHandler
{
   public void Handle(Exception exception) =>
      throw new InvalidOperationException("Unhandled exception in background task during testing.", exception);
}
