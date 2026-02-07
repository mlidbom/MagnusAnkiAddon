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

   internal App()
   {

      Services = AppBootstrapper.Bootstrap(this).Resolve<TemporaryServiceCollection>();
      Collection = Services.ServiceLocator.Resolve<JPCollection>();
   }

   public static bool IsTesting => TestEnvDetector.IsTesting;

   readonly List<Action> _initHooks = new();

   public void AddInitHook(Action hook) => _initHooks.Add(hook);

   public void Dispose() => Services.Dispose();

   public static App Bootstrap() => new App();

   public JapaneseConfig Config => Services.ConfigurationStore.Config();
   public JPCollection Collection { get; }

   internal static string UserFilesDir
   {
      get
      {
         var assemblyLocation = typeof(App).Assembly.Location;
         var assemblyDir = Path.GetDirectoryName(Path.GetDirectoryName(assemblyLocation)) ?? string.Empty;
         return Path.Combine(assemblyDir, "user_files");
      }
   }
}
