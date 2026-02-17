using System;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core;

public class CoreApp : IDisposable
{
   public TemporaryServiceCollection Services { get; }
   public IEnvironmentPaths Paths { get; }

   internal CoreApp(
      IEnvironmentPaths environmentPaths,
      IBackendNoteCreator? backendNoteCreator = null,
      IBackendDataLoader? backendDataLoader = null)
   {
      Paths = environmentPaths;
      Services = AppBootstrapper.Bootstrap(this, backendNoteCreator, backendDataLoader).Resolve<TemporaryServiceCollection>();
   }

   public static bool IsTesting => TestEnvDetector.IsTesting;

   public void Dispose()
   {
      Services.Dispose();
      (Paths as IDisposable)?.Dispose();
   }

   public static CoreApp Bootstrap(
      IBackendNoteCreator? backendNoteCreator = null,
      IBackendDataLoader? backendDataLoader = null,
      IEnvironmentPaths? environmentPaths = null)
   {
      ArgumentNullException.ThrowIfNull(environmentPaths);
      return new CoreApp(environmentPaths, backendNoteCreator, backendDataLoader);
   }

   public JapaneseConfig Config => Services.ConfigurationStore.Config();
   public JPCollection Collection => Services.ServiceLocator.Resolve<JPCollection>();
}
