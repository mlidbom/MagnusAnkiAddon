using System;
using System.Collections.Generic;
using System.IO;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core;

public class App : IDisposable
{
   readonly TemporaryServiceLocator _services;
   internal App(TemporaryServiceLocator services) => _services = services;

   public static bool IsTesting => ExPytest.IsTesting;

   static JPCollection? _collection;
   static IBackendNoteCreator? _backendNoteCreator;

   static readonly List<Action> _initHooks = new();

   public static void AddInitHook(Action hook)
   {
      _initHooks.Add(hook);
   }

   public void Dispose()
   {
      _services.Dispose();
      GC.Collect(2);
      GC.WaitForPendingFinalizers();
   }

   public static App Bootstrap() => AppBootstrapper.Bootstrap();

   public static JapaneseConfig Config() => ConfigurationValue.Config();

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
