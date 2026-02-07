using System;
using System.Threading;
using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;

namespace JAStudio.UI;

public class App : Application
{
    static readonly ManualResetEventSlim _initialized = new();

    public override void Initialize() => AvaloniaXamlLoader.Load(this);

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            // No main window - we're hosted by Anki/Python
            // Windows are shown on-demand via JAStudioAppRoot
        }

        base.OnFrameworkInitializationCompleted();
        _initialized.Set();
    }

    /// <summary>
    /// Block until Avalonia framework initialization has completed.
    /// </summary>
    public static void WaitForInitialization(TimeSpan timeout)
    {
        if (!_initialized.Wait(timeout))
        {
            throw new TimeoutException(
                $"Avalonia did not initialize within {timeout.TotalSeconds}s.");
        }
    }
}
