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
      _collection = Services.ServiceLocator.Resolve<JPCollection>();
   }

   public static bool IsTesting => TestEnvDetector.IsTesting;

   JPCollection _collection;

   readonly List<Action> _initHooks = new();

   public void AddInitHook(Action hook) => _initHooks.Add(hook);

   public void Dispose()
   {
      Services.Dispose();
      if(!TestEnvDetector.IsTesting) //When running for real we have gigabytes of memory used and we want to free it immediately when restarting the app.
      {
         GC.Collect(2);
         GC.WaitForPendingFinalizers();
      }
   }

   public static App Bootstrap() => new App();

   public JapaneseConfig Config() => Services.ConfigurationStore.Config();

   public JPCollection Col() => _collection;

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
