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

// ReSharper disable once UnusedType.Global used from python
public class JAStudioAnkiAppRoot
{
   readonly CoreApp _coreApp;
   CancellationTokenSource? _reloadCts;
   static readonly TimeSpan ReloadDebounceDelay = TimeSpan.FromMilliseconds(500);

   // Stored to keep the UI thread rooted (prevent GC). Not accessed directly.
#pragma warning disable CS0414
   Thread? _uiThread;
#pragma warning restore CS0414

   // ReSharper disable once MemberCanBePrivate.Global used from python
   public TemporaryServiceCollection Services => _coreApp.Services;

   // ReSharper disable once UnusedAutoPropertyAccessor.Global used from python
   public AnkiDialogs Dialogs { get; }

   // ReSharper disable once UnusedAutoPropertyAccessor.Global used from python
   public AnkiMenus Menus { get; }

   JAStudioAnkiAppRoot(CoreApp coreApp)
   {
      _coreApp = coreApp;
      Dialogs = new AnkiDialogs(coreApp);
      Menus = new AnkiMenus(coreApp.Services);
   }

   // ReSharper disable once UnusedMember.Global // ReSharper disable once UnusedAutoPropertyAccessor.Global used from python
   public static JAStudioAnkiAppRoot Initialize(string configJson, Action<string> configUpdateCallback)
   {
      if(!Environment.GetEnvironmentVariable("DEBUG_JASTUDIO").IsNullEmptyOrWhiteSpace())
      {
         Debugger.Launch();
      }

      var app = AppBootstrapper.BootstrapProduction(
         environmentPaths: new AnkiEnvironmentPaths(),
         backendNoteCreator: new AnkiBackendNoteCreator(),
         backendDataLoader: new AnkiBackendDataLoader(),
         cardOperationsFactory: idMap => new AnkiCardOperationsImpl(idMap),
         configJson: configJson,
         configUpdateCallback: configUpdateCallback);
      CompzeLogger.LogLevel = LogLevel.Info;

      var uiThread = new Thread(() =>
                     {
                        AppBuilder.Configure<UIApp>()
                                  .UsePlatformDetect()
                                  .StartWithClassicDesktopLifetime([], ShutdownMode.OnExplicitShutdown);
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

      UIApp.WaitForInitialization(TimeSpan.FromSeconds(30));

      var root = new JAStudioAnkiAppRoot(app) { _uiThread = uiThread };

      // TODO: urgent:  this is a wiring concern and should probably not be here
      root.Services.TaskRunner.SetUiScopePanelFactory((scopeTitle, depth, parentScope) =>
      {
         var viewModel = new TaskProgressScopeViewModel(scopeTitle, depth);
         if(parentScope != null)
         {
            Dispatcher.UIThread.Invoke(() => parentScope.ViewModel.Children.Add(viewModel));
            return new AvaloniaScopePanel(viewModel, topLevelPanel: null, parentScope);
         }

         var panel = Dispatcher.UIThread.Invoke(() => MultiTaskProgressDialog.CreateScopePanel(viewModel, depth));
         return new AvaloniaScopePanel(viewModel, panel, parentScope: null);
      });

      root.Services.TaskRunner.SetUiTaskRunnerFactory((scopePanel, labelText, allowCancel) =>
      {
         var avaloniaScope = (AvaloniaScopePanel)scopePanel;
         return new AvaloniaTaskProgressRunner(avaloniaScope.ViewModel, labelText, allowCancel);
      });

      //TODO: urgent: this is a bleeding mess of a dependency, implementing a vital part of a component through a callback here. Jeez!
      // Keep the progress dialog window open across nested task scopes
      root.Services.TaskRunner.SetDialogLifetimeCallbacks(
         () => Dispatcher.UIThread.Invoke(MultiTaskProgressDialog.Hold),
         () => Dispatcher.UIThread.Post(MultiTaskProgressDialog.Release));

      BackgroundTaskManagerSetup.Initialize();

      return root;
   }

   bool _profileOpen = false;

   // ReSharper disable once UnusedMember.Global used from python
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
               BackgroundTaskManager.Run(() => _coreApp.Collection.ReloadFromBackend());
            }

            break;

         case AnkiLifecycleEvent.ProfileClosing:
            _profileOpen = false;
            CancelPendingReload();
            _coreApp.Collection.ClearCaches();
            break;
         case AnkiLifecycleEvent.SyncStarting:
            CancelPendingReload();
            _coreApp.Collection.ClearCaches();
            break;

         default:
            throw new ArgumentOutOfRangeException(nameof(lifecycleEvent), lifecycleEvent, null);
      }
   }

   // ReSharper disable once UnusedMember.Global used from python
   public void ShutDown()
   {
      using var _ = this.Log().Info().LogMethodExecutionTime();
      _coreApp.Dispose();
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
         this.Log().Info("Debounce elapsed reloading from backend");
         _coreApp.Collection.ReloadFromBackend();
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

   /// <summary>
   /// Shutdown Avalonia. Call at addon unload.
   /// </summary>
   public void ShutdownUIFramework()
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
