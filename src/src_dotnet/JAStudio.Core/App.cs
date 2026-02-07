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
   internal App(TemporaryServiceCollection services) => Services = services;

   public static bool IsTesting => TestEnvDetector.IsTesting;

   JPCollection? _collection;
   IBackendNoteCreator? _backendNoteCreator;

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

   public static App Bootstrap() => AppBootstrapper.Bootstrap();

   public JapaneseConfig Config() => Services.ConfigurationStore.Config();

   public JPCollection Col()
   {
      if(_collection == null)
      {
         if(_backendNoteCreator == null)
         {
            throw new Exception("Backend note creator not initialized");
         }

         _collection = new JPCollection(_backendNoteCreator);
      }

      return _collection;
   }

   public void Reset(IBackendNoteCreator backendNoteCreator)
   {
      _collection = null;
      _backendNoteCreator = backendNoteCreator;
   }

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
