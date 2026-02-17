using System;

namespace JAStudio.Core.TaskRunners;

public interface IFatalErrorHandler
{
   void Handle(Exception exception);
}
