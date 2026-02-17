using System;
using Avalonia;
using JAStudio.Core;

namespace JAStudio.UI.DesktopHost;

class Program
{
   // Avalonia configuration, don't remove; also used by visual designer.
   public static AppBuilder BuildAvaloniaApp()
      => AppBuilder.Configure<UIApp>()
                   .UsePlatformDetect()
                   .LogToTrace();

   // The entry point. Things aren't ready yet, so at this point
   // you shouldn't use any Avalonia types or anything that expects
   // a SynchronizationContext to be ready
   [STAThread]
   public static int Main(string[] args)
   {
      AppBootstrapper.BootstrapForTests();
      return BuildAvaloniaApp()
        .StartWithClassicDesktopLifetime(args);
   }
}
