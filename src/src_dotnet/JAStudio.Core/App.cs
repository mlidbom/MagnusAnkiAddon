using System;
using System.Collections.Generic;
using System.IO;
using JAStudio.Core.Anki;
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
   }

   public static bool IsTesting => TestEnvDetector.IsTesting;

   readonly List<Action> _initHooks = new();

   public void AddInitHook(Action hook) => _initHooks.Add(hook);

   public void Dispose() => Services.Dispose();

   public static App Bootstrap() => new App();

   public JapaneseConfig Config => Services.ConfigurationStore.Config();
   public JPCollection Collection => Services.ServiceLocator.Resolve<JPCollection>();

   internal static string AddonRootDir
   {
      get
      {
         if (IsTesting)
         {
            var assemblyLocation = typeof(App).Assembly.Location;
            return Path.GetDirectoryName(Path.GetDirectoryName(assemblyLocation)) ?? string.Empty;
         }

         return AnkiFacade.GetAddonRootDir();
      }
   }

   internal static string UserFilesDir => Path.Combine(AddonRootDir, "user_files");

   internal static string DatabaseDir => Path.Combine(AddonRootDir, "jas_database");
}
