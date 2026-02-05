using System;
using System.Collections.Generic;
using System.Threading;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Threading;
using JAStudio.Core.Note;
using JAStudio.UI.Menus;
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
        Dispatcher.UIThread.Invoke(() =>
        {
            var window = new T();
            window.Show();
        });
    }

    /// <summary>
    /// Show the VocabFlagsDialog for editing a vocab note's flags.
    /// </summary>
    public static void ShowVocabFlagsDialog(int vocabId)
    {
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            var vocabCache = Core.App.Col().Vocab;
            var vocab = vocabCache.WithIdOrNone(vocabId);
            if (vocab == null)
            {
                JALogger.Log($"Vocab note with ID {vocabId} not found");
                return;
            }
            
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
        Dispatcher.UIThread.Invoke(() =>
        {
            var window = new AboutDialog();
            window.Show();
        });
    }

    /// <summary>
    /// Show the Options dialog for Japanese configuration settings.
    /// </summary>
    public static void ShowOptionsDialog()
    {
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            JALogger.Log("Creating OptionsDialog window...");
            var window = new OptionsDialog();
            JALogger.Log("OptionsDialog created, calling Show()...");
            window.Show();
            JALogger.Log("OptionsDialog.Show() completed");
        });
    }

    /// <summary>
    /// Show the Readings Mappings dialog for editing readings mappings.
    /// </summary>
    public static void ShowReadingsMappingsDialog()
    {
        JALogger.Log("ShowReadingsMappingsDialog() called");
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            var window = new ReadingsMappingsDialog();
            window.Show();
        });
    }

    /// <summary>
    /// Toggle the Note Search dialog visibility.
    /// Shows the dialog if hidden, hides it if visible.
    /// </summary>
    public static void ToggleNoteSearchDialog()
    {
        JALogger.Log("ToggleNoteSearchDialog() called");
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            NoteSearchDialog.ToggleVisibility();
        });
    }

    /// <summary>
    /// Toggle the English Word Search dialog visibility.
    /// Shows the dialog if hidden, hides it if visible.
    /// </summary>
    public static void ToggleEnglishWordSearchDialog()
    {
        JALogger.Log("ToggleEnglishWordSearchDialog() called");
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            EnglishWordSearchDialog.ToggleVisibility();
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
        Dispatcher.UIThread.Invoke(() =>
        {
            var menuControl = new ContextMenuPopup(clipboardContent ?? "", selectionContent ?? "");
            menuControl.ShowAt(x, y);
        });
    }

    /// <summary>
    /// Show the Japanese main menu at the specified screen coordinates.
    /// </summary>
    /// <param name="refreshCallback">Callback to invoke Anki UI refresh</param>
    /// <param name="executeLookup">Callback to execute an Anki search query</param>
    /// <param name="searchText">Text to use for searches (from selection or clipboard)</param>
    /// <param name="x">X coordinate in physical (device) pixels</param>
    /// <param name="y">Y coordinate in physical (device) pixels</param>
    public static void ShowJapaneseMainMenu(
        string searchText,
        int x, 
        int y)
    {
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            var menuBuilder = new JapaneseMainMenu(searchText ?? "");
            var menuItems = menuBuilder.BuildMenu();
            
            PopupMenuHost.ShowAt(menuItems, x, y);
        });
    }

    /// <summary>
    /// Show context menu for a vocab note.
    /// </summary>
    public static void ShowVocabContextMenu(
        int vocabId,
        string selection, 
        string clipboard, 
        int x, 
        int y)
    {
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            var menuBuilder = new NoteContextMenu();
            var menuItems = menuBuilder.BuildVocabContextMenu(vocabId, selection ?? "", clipboard ?? "");
            
            PopupMenuHost.ShowAt(menuItems, x, y);
        });
    }

    /// <summary>
    /// Show context menu for a kanji note.
    /// </summary>
    public static void ShowKanjiContextMenu(
        int kanjiId,
        string selection, 
        string clipboard, 
        int x, 
        int y)
    {
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            var menuBuilder = new NoteContextMenu();
            var menuItems = menuBuilder.BuildKanjiContextMenu(kanjiId, selection ?? "", clipboard ?? "");
            
            PopupMenuHost.ShowAt(menuItems, x, y);
        });
    }

    /// <summary>
    /// Show context menu for a sentence note.
    /// </summary>
    public static void ShowSentenceContextMenu(
        int sentenceId,
        string selection, 
        string clipboard, 
        int x, 
        int y)
    {
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            var menuBuilder = new NoteContextMenu();
            var menuItems = menuBuilder.BuildSentenceContextMenu(sentenceId, selection ?? "", clipboard ?? "");
            
            PopupMenuHost.ShowAt(menuItems, x, y);
        });
    }

    /// <summary>
    /// Show context menu when no note is available.
    /// </summary>
    public static void ShowGenericContextMenu(
        string selection, 
        string clipboard, 
        int x, 
        int y)
    {
        EnsureInitialized();
        Dispatcher.UIThread.Invoke(() =>
        {
            var menuBuilder = new NoteContextMenu();
            var menuItems = menuBuilder.BuildGenericContextMenu(selection ?? "", clipboard ?? "");
            
            PopupMenuHost.ShowAt(menuItems, x, y);
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
        Dispatcher.UIThread.Invoke(() =>
        {
            var item1 = new MenuItem { Header = "Test Item 1" };
            item1.Click += (s, e) => JALogger.Log("Test Item 1 clicked from main menu");
            
            var item2 = new MenuItem { Header = "Test Item 2" };
            item2.Click += (s, e) => JALogger.Log("Test Item 2 clicked from main menu");
            
            var menuItems = new List<MenuItem> { item1, item2 };
            
            PopupMenuHost.ShowAt(menuItems, x, y);
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
        Dispatcher.UIThread.Invoke(() =>
        {
            var selectionText = string.IsNullOrEmpty(selection) ? "(empty)" : selection;
            var clipboardText = string.IsNullOrEmpty(clipboard) ? "(empty)" : clipboard;
            
            var selectionItem = new MenuItem { Header = $"Selection: {TruncateText(selectionText, 30)}" };
            selectionItem.Click += (s, e) => JALogger.Log($"Selection clicked: {selection}");
            
            var clipboardItem = new MenuItem { Header = $"Clipboard: {TruncateText(clipboardText, 30)}" };
            clipboardItem.Click += (s, e) => JALogger.Log($"Clipboard clicked: {clipboard}");
            
            var menuItems = new List<MenuItem> { selectionItem, clipboardItem };
            
            PopupMenuHost.ShowAt(menuItems, x, y);
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

        Dispatcher.UIThread.Invoke(() =>
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
