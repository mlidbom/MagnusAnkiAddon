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

   static JPCollection? _collection;
   static IBackendNoteCreator? _backendNoteCreator;

   static readonly List<Action> _initHooks = new();

   public static void AddInitHook(Action hook)
   {
      _initHooks.Add(hook);
   }

   public void Dispose()
   {
      Services.Dispose();
      GC.Collect(2);
      GC.WaitForPendingFinalizers();
   }

   public static App Bootstrap() => AppBootstrapper.Bootstrap();

   public static void InitConfigForTesting() => ConfigurationStore.InitForTesting();
   public static void InitConfigJson(string json, Action<string> updateCallback) => ConfigurationStore.InitJson(json, updateCallback);
   public static JapaneseConfig Config() => ConfigurationStore.Config();

   public static JPCollection Col()
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

   public static void Reset(IBackendNoteCreator backendNoteCreator)
   {
      _collection = null;
      _backendNoteCreator = backendNoteCreator;
   }

   public static string UserFilesDir
   {
      get
      {
         var assemblyLocation = typeof(App).Assembly.Location;
         var assemblyDir = Path.GetDirectoryName(Path.GetDirectoryName(assemblyLocation)) ?? string.Empty;
         return Path.Combine(assemblyDir, "user_files");
      }
   }
}
