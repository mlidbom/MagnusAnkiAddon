using System;
using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using JAStudio.Core.TestUtils;
using JAStudio.UI;
using JAStudio.UI.Views;

namespace JAStudio.UI.DesktopHost;

class Program
{
    // Avalonia configuration, don't remove; also used by visual designer.
    public static AppBuilder BuildAvaloniaApp()
        => AppBuilder.Configure<App>()
            .UsePlatformDetect()
            .LogToTrace();

    // The entry point. Things aren't ready yet, so at this point
    // you shouldn't use any Avalonia types or anything that expects
    // a SynchronizationContext to be ready
    [STAThread]
    public static int Main(string[] args)
    {
       TestApp.Reset();
       return BuildAvaloniaApp()
         .StartWithClassicDesktopLifetime(args);
    }
}
