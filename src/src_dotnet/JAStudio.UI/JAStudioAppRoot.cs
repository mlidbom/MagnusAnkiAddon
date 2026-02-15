using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Threading;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE;
using JAStudio.Anki;
using JAStudio.Core;
using JAStudio.Core.TaskRunners;
using JAStudio.UI.Dialogs;
using JAStudio.UI.Utils;

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
   CancellationTokenSource? _reloadCts;
   static readonly TimeSpan ReloadDebounceDelay = TimeSpan.FromMilliseconds(500);

   // Stored to keep the UI thread rooted (prevent GC). Not accessed directly.
#pragma warning disable CS0414
   Thread? _uiThread;
#pragma warning restore CS0414

   /// <summary>
   /// The resolved service collection, derived from the bootstrapped Core.App.
   /// Used by dialog code-behinds to pass services to their ViewModels.
   /// </summary>
   public TemporaryServiceCollection Services => _app.Services;

   /// <summary>Dialog show/toggle methods, extracted from this root.</summary>
   public AppDialogs Dialogs { get; }

   /// <summary>Menu factory methods, extracted from this root.</summary>
   public AppMenus Menus { get; }

   JAStudioAppRoot(Core.App app)
   {
      _app = app;
      Dialogs = new AppDialogs(app);
      Menus = new AppMenus(app.Services, Dialogs);
   }

   /// <summary>
   /// Bootstrap Core.App, initialize Avalonia, and return the composition root.
   /// Call once at addon startup.
   /// </summary>
   /// <param name="configJson">JSON-serialized configuration dictionary from the Anki addon.</param>
   /// <param name="configUpdateCallback">Callback that receives updated config JSON to persist back to Anki.</param>
   public static JAStudioAppRoot Initialize(string configJson, Action<string> configUpdateCallback)
   {
      if(!Environment.GetEnvironmentVariable("DEBUG_JASTUDIO").IsNullEmptyOrWhiteSpace())
      {
         Debugger.Launch();
      }

      var app = Core.App.Bootstrap(
         backendNoteCreator: new AnkiBackendNoteCreator(),
         backendDataLoader: new AnkiBackendDataLoader(),
         environmentPaths: new AnkiEnvironmentPaths());
      CompzeLogger.LogLevel = LogLevel.Info;

      // Initialize the C# configuration system with the Anki addon config
      app.Services.ConfigurationStore.InitJson(configJson, configUpdateCallback);

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

      // Set up task runner factories
      root.Services.TaskRunner.SetUiScopePanelFactory((scopeTitle, depth) =>
      {
         var viewModel = new TaskProgressScopeViewModel(scopeTitle);
         var panel = Dispatcher.UIThread.Invoke(() => MultiTaskProgressDialog.CreateScopePanel(viewModel, depth));
         return new AvaloniaScopePanel(viewModel, panel);
      });

      root.Services.TaskRunner.SetUiTaskRunnerFactory((scopePanel, labelText, allowCancel) =>
      {
         var avaloniaScope = (AvaloniaScopePanel)scopePanel;
         return new AvaloniaTaskProgressRunner(avaloniaScope.ViewModel, labelText, allowCancel);
      });

      // Keep the progress dialog window open across nested task scopes
      root.Services.TaskRunner.SetDialogLifetimeCallbacks(
         () => Dispatcher.UIThread.Invoke(() => MultiTaskProgressDialog.Hold()),
         () => Dispatcher.UIThread.Post(() => MultiTaskProgressDialog.Release()));

      BackgroundTaskManagerSetup.Initialize();

      // Register card operations so Core can suspend/unsuspend cards via the backend API
      root.Services.CardOperations.SetImplementation(new AnkiCardOperationsImpl(root.Services.ExternalNoteIdMap));

      return root;
   }

   bool _profileOpen = false;

   /// <summary>
   /// Handle a lifecycle event from the Anki host.
   /// Python calls this instead of managing complex init/destruct cycles.
   /// </summary>
   /// <remarks>
   /// Reload events are debounced: when Anki starts it often fires ProfileOpened
   /// immediately followed by SyncStarting → SyncCompleted, so we wait briefly
   /// before actually loading to avoid redundant expensive reloads.
   /// Clear events (SyncStarting, ProfileClosing) cancel any pending reload and
   /// clear caches immediately.
   /// </remarks>
   public void HandleAnkiLifecycleEvent(AnkiLifecycleEvent lifecycleEvent)
   {
      this.Log().Info($"HandleAnkiLifecycleEvent({lifecycleEvent})");

      switch(lifecycleEvent)
      {
         case AnkiLifecycleEvent.ProfileOpened:
            _profileOpen = true;
            ScheduleDebouncedReload();
            break;

         case AnkiLifecycleEvent.SyncCompleted:
            if(_profileOpen)
            {
               CancelPendingReload();
               BackgroundTaskManager.Run(() => _app.Collection.ReloadFromBackend());
            }

            break;

         case AnkiLifecycleEvent.ProfileClosing:
            _profileOpen = false;
            CancelPendingReload();
            _app.Collection.ClearCaches();
            break;
         case AnkiLifecycleEvent.SyncStarting:
            CancelPendingReload();
            _app.Collection.ClearCaches();
            break;

         default:
            throw new ArgumentOutOfRangeException(nameof(lifecycleEvent), lifecycleEvent, null);
      }
   }

   public void ShutDown()
   {
      using var _ = this.Log().Info().LogMethodExecutionTime();
      _app.Dispose();
      Dispatcher.UIThread.InvokeShutdown();
   }

   void ScheduleDebouncedReload()
   {
      CancelPendingReload();
      var cts = new CancellationTokenSource();
      _reloadCts = cts;

      BackgroundTaskManager.RunAsync(async () =>
      {
         await Task.Delay(ReloadDebounceDelay, cts.Token);
         this.Log().Info("Debounce elapsed \u2014 reloading from backend");
         _app.Collection.ReloadFromBackend();
      });
   }

   void CancelPendingReload()
   {
      if(_reloadCts != null)
      {
         _reloadCts.Cancel();
         _reloadCts.Dispose();
         _reloadCts = null;
      }
   }

   // ── UI thread helpers ──

   /// <summary>
   /// Run an action on the Avalonia UI thread.
   /// </summary>
   public void RunOnUIThread(Action action)
   {
      Dispatcher.UIThread.Post(action);
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
