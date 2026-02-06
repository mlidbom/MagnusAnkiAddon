using System;
using System.Collections.Generic;
using System.IO;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.TestUtils;
using Newtonsoft.Json;

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

   // --- Configuration store (moved from ConfigurationValue) ---

   static Dictionary<string, object>? _configDict;
   static Action<string>? _updateCallback;
   internal static Dictionary<string, string>? StaticReadingsMappings;

   public static void InitConfigForTesting()
   {
      if(_configDict != null) return;
      InitConfigJson("{}", s => {});
      StaticReadingsMappings = new Dictionary<string, string>();
   }

   public static void InitConfigJson(string json, Action<string> updateCallback)
   {
      if(_configDict != null)
      {
         throw new InvalidOperationException("Configuration dict already initialized");
      }

      _configDict = JsonConvert.DeserializeObject<Dictionary<string, object>>(json);
      _updateCallback = updateCallback;
   }

   internal static Dictionary<string, object> GetConfigDict()
   {
      if(IsTesting)
      {
         return new Dictionary<string, object>();
      }

      if(_configDict == null)
      {
         throw new InvalidOperationException("Configuration dict not initialized");
      }

      return _configDict;
   }

   internal static void WriteConfigDict()
   {
      if(!IsTesting && _updateCallback != null && _configDict != null)
      {
         var json = JsonConvert.SerializeObject(_configDict, Formatting.None);
         _updateCallback(json);
      }
   }

   static JapaneseConfig? _config;

   public static JapaneseConfig Config()
   {
      return _config ??= new JapaneseConfig();
   }

   // --- End configuration store ---

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
