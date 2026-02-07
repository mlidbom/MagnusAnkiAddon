using System;
using System.Threading;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Threading;
using JAStudio.Core.TaskRunners;
using JAStudio.UI.Dialogs;
using JAStudio.UI.Menus;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Views;

namespace JAStudio.UI;

/// <summary>
/// Entry point for Python to interact with Avalonia UI.
/// Call Initialize() once at startup, then use Show*Dialog() methods.
/// </summary>
public static class DialogHost
{
   static bool _initialized;
   static Thread? _uiThread;
   static AutoResetEvent? _initEvent;

   /// <summary>
   /// Initialize Avalonia. Call once at addon startup.
   /// </summary>
   public static void Initialize()
   {
      if(_initialized) return;

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

      if(OperatingSystem.IsWindows())
      {
         _uiThread.SetApartmentState(ApartmentState.STA);
      }

      _uiThread.Start();

      // Wait for Avalonia to initialize
      // TODO: Add proper synchronization with App.OnFrameworkInitializationCompleted
      Thread.Sleep(500);

      // Set up task runner factory
      TaskRunner.SetUiTaskRunnerFactory((windowTitle, labelText, allowCancel, modal) =>
                                           new AvaloniaTaskProgressRunner(windowTitle, labelText, allowCancel, modal));

      // Register Anki card operations so Core can suspend/unsuspend cards via Anki API
      Core.TemporaryServiceCollection.Instance.AnkiCardOperations.SetImplementation(new Anki.AnkiCardOperationsImpl());

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
         if(vocab == null)
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
   /// Build browser context menu specification.
   /// Returns UI-agnostic menu specs that Python can convert to PyQt menus.
   /// </summary>
   /// <param name="selectedCardIds">List of selected card IDs (dynamic from Python)</param>
   /// <param name="selectedNoteIds">List of selected note IDs (dynamic from Python)</param>
   public static SpecMenuItem BuildBrowserMenuSpec(
      dynamic selectedCardIds,
      dynamic selectedNoteIds)
   {
      EnsureInitialized();
      return BrowserMenus.BuildBrowserMenuSpec(selectedCardIds, selectedNoteIds);
   }

   /// <summary>
   /// Shutdown Avalonia. Call at addon unload.
   /// </summary>
   public static void Shutdown()
   {
      if(!_initialized) return;

      Dispatcher.UIThread.Invoke(() =>
      {
         if(Application.Current?.ApplicationLifetime is IClassicDesktopStyleApplicationLifetime lifetime)
         {
            lifetime.Shutdown();
         }
      });

      _initialized = false;
   }

   static void EnsureInitialized()
   {
      if(!_initialized)
         throw new InvalidOperationException("DialogHost.Initialize() must be called before showing dialogs.");
   }
}
