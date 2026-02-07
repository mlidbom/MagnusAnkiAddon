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
/// Bootstraps Core.App, initializes Avalonia, and provides factory methods
/// for creating menus and showing dialogs.
/// Python calls Initialize() once at startup, then uses the returned instance.
/// </summary>
public class JAStudioAppRoot
{
   readonly Core.App _app;
   // Stored to keep the UI thread rooted (prevent GC). Not accessed directly.
#pragma warning disable CS0414
   Thread? _uiThread;
#pragma warning restore CS0414

   /// <summary>
   /// The resolved service collection, derived from the bootstrapped Core.App.
   /// Used by dialog code-behinds to pass services to their ViewModels.
   /// </summary>
   public Core.TemporaryServiceCollection Services => _app.Services;

   JAStudioAppRoot(Core.App app) => _app = app;

   /// <summary>
   /// Bootstrap Core.App, initialize Avalonia, and return the composition root.
   /// Call once at addon startup.
   /// </summary>
   public static JAStudioAppRoot Initialize()
   {
      var app = Core.App.Bootstrap();

      var initEvent = new AutoResetEvent(false);

      var uiThread = new Thread(() =>
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
         uiThread.SetApartmentState(ApartmentState.STA);
      }

      uiThread.Start();

      // Wait for Avalonia to finish framework initialization
      App.WaitForInitialization(TimeSpan.FromSeconds(30));

      var root = new JAStudioAppRoot(app) { _uiThread = uiThread };

      // Set up task runner factory
      root.Services.TaskRunner.SetUiTaskRunnerFactory((windowTitle, labelText, allowCancel, modal) =>
                                           new AvaloniaTaskProgressRunner(windowTitle, labelText, allowCancel, modal));

      // Register Anki card operations so Core can suspend/unsuspend cards via Anki API
      root.Services.AnkiCardOperations.SetImplementation(new Anki.AnkiCardOperationsImpl());

      return root;
   }

   // ── Factory methods for Python-facing objects ──

   /// <summary>
   /// Create a NoteContextMenu wired with all required services.
   /// Called from Python to build right-click context menus.
   /// </summary>
   public NoteContextMenu CreateNoteContextMenu() => new(Services);

   /// <summary>
   /// Create a JapaneseMainMenu wired with all required services.
   /// Called from Python to build the main "Japanese" tools menu.
   /// </summary>
   public JapaneseMainMenu CreateJapaneseMainMenu() => new(this);

   // ── UI thread helpers ──

   /// <summary>
   /// Run an action on the Avalonia UI thread.
   /// </summary>
   public void RunOnUIThread(Action action)
   {
      Dispatcher.UIThread.Post(action);
   }

   /// <summary>
   /// Show a dialog and wait for it to close.
   /// </summary>
   public void ShowDialog<T>() where T : Window, new()
   {
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
   public void ShowVocabFlagsDialog(int vocabId)
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         var vocabCache = _app.Col().Vocab;
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
   public void ShowAboutDialog()
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         var window = new AboutDialog();
         window.Show();
      });
   }

   /// <summary>
   /// Show the Options dialog for Japanese configuration settings.
   /// </summary>
   public void ShowOptionsDialog()
   {
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
   public void ShowReadingsMappingsDialog()
   {
      JALogger.Log("ShowReadingsMappingsDialog() called");
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
   public void ToggleNoteSearchDialog()
   {
      JALogger.Log("ToggleNoteSearchDialog() called");
      Dispatcher.UIThread.Invoke(() =>
      {
         NoteSearchDialog.ToggleVisibility(Services);
      });
   }

   /// <summary>
   /// Toggle the English Word Search dialog visibility.
   /// Shows the dialog if hidden, hides it if visible.
   /// </summary>
   public void ToggleEnglishWordSearchDialog()
   {
      JALogger.Log("ToggleEnglishWordSearchDialog() called");
      Dispatcher.UIThread.Invoke(() =>
      {
         EnglishWordSearchDialog.ToggleVisibility();
      });
   }

   /// <summary>
   /// Show the context menu popup at the current cursor position.
   /// </summary>
   public void ShowContextMenuPopup(string clipboardContent, string selectionContent, int x, int y)
   {
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
   public SpecMenuItem BuildBrowserMenuSpec(
      dynamic selectedCardIds,
      dynamic selectedNoteIds)
   {
      return new BrowserMenus(Services).BuildBrowserMenuSpec(selectedCardIds, selectedNoteIds);
   }

   /// <summary>
   /// Shutdown Avalonia. Call at addon unload.
   /// </summary>
   public void Shutdown()
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         if(Application.Current?.ApplicationLifetime is IClassicDesktopStyleApplicationLifetime lifetime)
         {
            lifetime.Shutdown();
         }
      });
   }
}
