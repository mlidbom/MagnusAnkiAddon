using System;
using System.Threading;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Threading;
using JAStudio.Core.Note;
using JAStudio.UI.Views;

namespace JAStudio.UI;

/// <summary>
/// Entry point for Python to interact with Avalonia UI.
/// Call Initialize() once at startup, then use Show*Dialog() methods.
/// </summary>
public static class DialogHost
{
    private static bool _initialized;
    private static Thread? _uiThread;
    private static AutoResetEvent? _initEvent;

    /// <summary>
    /// Initialize Avalonia. Call once at addon startup.
    /// </summary>
    public static void Initialize()
    {
        if (_initialized) return;

        _initEvent = new AutoResetEvent(false);

        _uiThread = new Thread(() =>
        {
            AppBuilder.Configure<App>()
                .UsePlatformDetect()
                .StartWithClassicDesktopLifetime(Array.Empty<string>(), ShutdownMode.OnExplicitShutdown);
        })
        {
            IsBackground = true,
            Name = "AvaloniaUIThread"
        };

        if (OperatingSystem.IsWindows())
        {
            _uiThread.SetApartmentState(ApartmentState.STA);
        }
        _uiThread.Start();

        // Wait for Avalonia to initialize
        // TODO: Add proper synchronization with App.OnFrameworkInitializationCompleted
        Thread.Sleep(500);
        _initialized = true;
    }

    /// <summary>
    /// Run an action on the Avalonia UI thread.
    /// </summary>
    public static void RunOnUIThread(Action action)
    {
        EnsureInitialized();
        Dispatcher.UIThread.Post(action);
    }

    /// <summary>
    /// Show a dialog and wait for it to close.
    /// </summary>
    public static void ShowDialog<T>() where T : Window, new()
    {
        EnsureInitialized();
        Dispatcher.UIThread.InvokeAsync(() =>
        {
            var window = new T();
            window.Show();
        });
    }

    /// <summary>
    /// Show the VocabFlagsDialog for editing a vocab note's flags.
    /// </summary>
    public static void ShowVocabFlagsDialog(VocabNote vocab)
    {
        EnsureInitialized();
        Dispatcher.UIThread.InvokeAsync(() =>
        {
            var window = new VocabFlagsDialog(vocab);
            window.Show();
        });
    }

    /// <summary>
    /// Show the About dialog.
    /// </summary>
    public static void ShowAboutDialog()
    {
        EnsureInitialized();
        Dispatcher.UIThread.InvokeAsync(() =>
        {
            var window = new AboutDialog();
            window.Show();
        });
    }

    /// <summary>
    /// Shutdown Avalonia. Call at addon unload.
    /// </summary>
    public static void Shutdown()
    {
        if (!_initialized) return;

        Dispatcher.UIThread.InvokeAsync(() =>
        {
            if (Application.Current?.ApplicationLifetime is IClassicDesktopStyleApplicationLifetime lifetime)
            {
                lifetime.Shutdown();
            }
        });

        _initialized = false;
    }

    private static void EnsureInitialized()
    {
        if (!_initialized)
            throw new InvalidOperationException("DialogHost.Initialize() must be called before showing dialogs.");
    }
}
