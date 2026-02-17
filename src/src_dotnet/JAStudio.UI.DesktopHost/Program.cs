using System;
using Avalonia;
using JAStudio.Core.TestUtils;

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
      TestCoreApp.Reset();
      return BuildAvaloniaApp()
        .StartWithClassicDesktopLifetime(args);
   }
}
