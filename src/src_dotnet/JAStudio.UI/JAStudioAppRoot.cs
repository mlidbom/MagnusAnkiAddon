using System;
using System.Threading;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Threading;
using JAStudio.UI.Dialogs;
using JAStudio.UI.Menus;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Views;

namespace JAStudio.UI;

/// <summary>
/// Composition root for the Anki addon.
/// Bootstraps the domain App, initializes Avalonia, and provides factory methods
/// for creating menus and showing dialogs.
/// Python calls Initialize() once at startup, then uses the factory/show methods.
/// </summary>
public static class JAStudioAppRoot
{
   static bool _initialized;
   static Thread? _uiThread;
   static AutoResetEvent? _initEvent;

   /// <summary>
   /// The resolved service collection. Available after Initialize() has been called.
   /// Used by dialog code-behinds to pass services to their ViewModels.
   /// </summary>
   public static Core.TemporaryServiceCollection Services { get; private set; } = null!;

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

      Services = Core.TemporaryServiceCollection.Instance;

      // Set up task runner factory
      Services.TaskRunner.SetUiTaskRunnerFactory((windowTitle, labelText, allowCancel, modal) =>
                                           new AvaloniaTaskProgressRunner(windowTitle, labelText, allowCancel, modal));

      // Register Anki card operations so Core can suspend/unsuspend cards via Anki API
      Services.AnkiCardOperations.SetImplementation(new Anki.AnkiCardOperationsImpl());

      _initialized = true;
   }

   // ── Factory methods for Python-facing objects ──

   /// <summary>
   /// Create a NoteContextMenu wired with all required services.
   /// Called from Python to build right-click context menus.
   /// </summary>
   public static NoteContextMenu CreateNoteContextMenu() => new(Services);

   /// <summary>
   /// Create a JapaneseMainMenu wired with all required services.
   /// Called from Python to build the main "Japanese" tools menu.
   /// </summary>
   public static JapaneseMainMenu CreateJapaneseMainMenu() => new(Services);

   // ── UI thread helpers ──

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

   // ── Dialog show methods (called from Python and C# menus) ──

   /// <summary>
   /// Show the VocabFlagsDialog for editing a vocab note's flags.
   /// </summary>
   public static void ShowVocabFlagsDialog(int vocabId)
   {
      EnsureInitialized();
      Dispatcher.UIThread.Invoke(() =>
      {
         var vocabCache = Services.App.Col().Vocab;
         var vocab = vocabCache.WithIdOrNone(vocabId);
         if(vocab == null)
         {
            JALogger.Log($"Vocab note with ID {vocabId} not found");
            return;
         }

         var window = new VocabFlagsDialog(vocab, Services);
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
         var window = new OptionsDialog(Services);
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
         var window = new ReadingsMappingsDialog(Services);
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
         NoteSearchDialog.ToggleVisibility(Services);
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
   public static SpecMenuItem BuildBrowserMenuSpec(
      dynamic selectedCardIds,
      dynamic selectedNoteIds)
   {
      EnsureInitialized();
      return new BrowserMenus(Services).BuildBrowserMenuSpec(selectedCardIds, selectedNoteIds);
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
         throw new InvalidOperationException("JAStudioAppRoot.Initialize() must be called before showing dialogs.");
   }
}
