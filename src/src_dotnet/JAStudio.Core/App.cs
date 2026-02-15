using System;
using System.Collections.Generic;
using System.IO;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core;

public class App : IDisposable
{
   public TemporaryServiceCollection Services { get; }

   static IEnvironmentPaths? _environmentPaths;

   internal App(
      IBackendNoteCreator? backendNoteCreator = null,
      IBackendDataLoader? backendDataLoader = null) =>
      Services = AppBootstrapper.Bootstrap(this, backendNoteCreator, backendDataLoader).Resolve<TemporaryServiceCollection>();

   public static bool IsTesting => TestEnvDetector.IsTesting;

   readonly List<Action> _initHooks = new();

   public void AddInitHook(Action hook) => _initHooks.Add(hook);

   public void Dispose() => Services.Dispose();

   public static App Bootstrap(
      IBackendNoteCreator? backendNoteCreator = null,
      IBackendDataLoader? backendDataLoader = null,
      IEnvironmentPaths? environmentPaths = null)
   {
      if(environmentPaths != null) _environmentPaths = environmentPaths;
      return new App(backendNoteCreator, backendDataLoader);
   }

   public JapaneseConfig Config => Services.ConfigurationStore.Config();
   public JPCollection Collection => Services.ServiceLocator.Resolve<JPCollection>();

   internal static string AddonRootDir
   {
      get
      {
         if(IsTesting)
         {
            var assemblyLocation = typeof(App).Assembly.Location;
            return Path.GetDirectoryName(Path.GetDirectoryName(assemblyLocation)) ?? string.Empty;
         }

         return _environmentPaths?.AddonRootDir
             ?? throw new InvalidOperationException("IEnvironmentPaths must be provided for non-testing mode. Call App.Bootstrap() with an IEnvironmentPaths implementation.");
      }
   }

   internal static string UserFilesDir => Path.Combine(AddonRootDir, "user_files");

   internal static string DatabaseDir => Path.Combine(AddonRootDir, "jas_database");

   internal static string AnkiMediaDir =>
      _environmentPaths?.AnkiMediaDir
   ?? throw new InvalidOperationException("IEnvironmentPaths must be provided for non-testing mode. Call App.Bootstrap() with an IEnvironmentPaths implementation.");
}
