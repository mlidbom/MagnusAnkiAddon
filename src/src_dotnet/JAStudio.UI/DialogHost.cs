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
    /// Show the context menu popup at the current cursor position.
    /// </summary>
    /// <param name="clipboardContent">Content from clipboard</param>
    /// <param name="selectionContent">Currently selected text</param>
    /// <param name="x">X coordinate for popup position (screen coordinates)</param>
    /// <param name="y">Y coordinate for popup position (screen coordinates)</param>
    public static void ShowContextMenuPopup(string clipboardContent, string selectionContent, int x, int y)
    {
        EnsureInitialized();
        Dispatcher.UIThread.InvokeAsync(() =>
        {
            var menuControl = new ContextMenuPopup(clipboardContent ?? "", selectionContent ?? "");
            menuControl.ShowAt(x, y);
        });
    }

    /// <summary>
    /// Show the test main menu ("Japanese Avalonia") at the specified screen coordinates.
    /// Menu is entirely defined in C#.
    /// </summary>
    /// <param name="x">X coordinate in physical (device) pixels</param>
    /// <param name="y">Y coordinate in physical (device) pixels</param>
    public static void ShowTestMainMenu(int x, int y)
    {
        EnsureInitialized();
        Dispatcher.UIThread.InvokeAsync(() =>
        {
            var builder = new AvaloniaMenuBuilder();
            
            builder.AddItem("Test Item 1", () =>
            {
                JALogger.Log("Test Item 1 clicked from main menu");
            });
            
            builder.AddItem("Test Item 2", () =>
            {
                JALogger.Log("Test Item 2 clicked from main menu");
            });
            
            builder.ShowAt(x, y);
        });
    }

    /// <summary>
    /// Show the test context menu with selection and clipboard options.
    /// Menu is entirely defined in C#.
    /// </summary>
    /// <param name="selection">Currently selected text</param>
    /// <param name="clipboard">Clipboard content</param>
    /// <param name="x">X coordinate in physical (device) pixels</param>
    /// <param name="y">Y coordinate in physical (device) pixels</param>
    public static void ShowTestContextMenu(string selection, string clipboard, int x, int y)
    {
        EnsureInitialized();
        Dispatcher.UIThread.InvokeAsync(() =>
        {
            var builder = new AvaloniaMenuBuilder();
            
            var selectionText = string.IsNullOrEmpty(selection) ? "(empty)" : selection;
            builder.AddItem($"Selection: {TruncateText(selectionText, 30)}", () =>
            {
                JALogger.Log($"Selection clicked: {selection}");
            });
            
            var clipboardText = string.IsNullOrEmpty(clipboard) ? "(empty)" : clipboard;
            builder.AddItem($"Clipboard: {TruncateText(clipboardText, 30)}", () =>
            {
                JALogger.Log($"Clipboard clicked: {clipboard}");
            });
            
            builder.ShowAt(x, y);
        });
    }

    private static string TruncateText(string text, int maxLength)
    {
        if (text.Length <= maxLength)
            return text;
        return text.Substring(0, maxLength) + "...";
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
