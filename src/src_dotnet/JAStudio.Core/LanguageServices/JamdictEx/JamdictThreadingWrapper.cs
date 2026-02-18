using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using JAStudio.Core.Configuration;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.Core.LanguageServices.JamdictEx;

class Request<T>
{
   public Func<dynamic, T> Func { get; }
   public TaskCompletionSource<T> TaskCompletionSource { get; }

   public Request(Func<dynamic, T> func, TaskCompletionSource<T> taskCompletionSource)
   {
      Func = func;
      TaskCompletionSource = taskCompletionSource;
   }
}

class JamdictLookupResult
{
   public List<DictEntry> Entries { get; }
   public List<DictEntry> Names { get; }

   public JamdictLookupResult(List<DictEntry> entries, List<DictEntry> names)
   {
      Entries = entries;
      Names = names;
   }
}

class JamdictThreadingWrapper : IDisposable
{
   static readonly object Lock = new();
   static JamdictThreadingWrapper? _instance;

   public static JamdictThreadingWrapper GetInstance(JapaneseConfig config)
   {
      if(_instance != null) return _instance;
      lock(Lock)
      {
         return _instance ??= new JamdictThreadingWrapper(config);
      }
   }

   public static void ShutDown()
   {
      lock(Lock)
      {
         _instance?.Dispose();
         _instance = null;
      }
   }

   readonly BlockingCollection<object> _queue;

   // ReSharper disable once PrivateFieldCanBeConvertedToLocalVariable
   readonly Thread _thread;
   dynamic? _jamdict;
   volatile bool _running;
   readonly JapaneseConfig _config;

   JamdictThreadingWrapper(JapaneseConfig config)
   {
      _config = config;
      _running = true;
      _queue = new BlockingCollection<object>();
      _thread = new Thread(Worker) { IsBackground = true };
      _thread.Start();
   }

   public void Dispose()
   {
      _running = false;
      _queue.CompleteAdding();
      _thread.Join(TimeSpan.FromSeconds(5));
      _queue.Dispose();
   }

   dynamic CreateJamdict()
   {
      // NOTE: Caller must already hold the GIL
      dynamic jamdictModule = Py.Import("jamdict");

      var memoryMode = _config.LoadJamdictDbIntoMemory.Value && !CoreApp.IsTesting;

      if(memoryMode)
      {
         return jamdictModule.Jamdict(memory_mode: true);
      } else
      {
         return jamdictModule.Jamdict(reuse_ctx: true);
      }
   }

   dynamic GetJamdict()
   {
      // NOTE: Caller must already hold the GIL
      if(_jamdict == null)
      {
         _jamdict = CreateJamdict();
      }

      return _jamdict;
   }

   void Worker()
   {
      while(_running)
      {
         try
         {
            // Wait for request WITHOUT holding GIL
            var request = _queue.Take();

            // Acquire GIL only for processing this request
            using(PythonEnvironment.LockGil())
            {
               try
               {
                  if(request is Request<JamdictLookupResult> lookupRequest)
                  {
                     var result = lookupRequest.Func(GetJamdict());
                     lookupRequest.TaskCompletionSource.SetResult(result);
                  } else if(request is Request<List<string>> stringListRequest)
                  {
                     var result = stringListRequest.Func(GetJamdict());
                     stringListRequest.TaskCompletionSource.SetResult(result);
                  }
               }
               catch(Exception e)
               {
                  if(request is Request<JamdictLookupResult> lookupRequest)
                  {
                     lookupRequest.TaskCompletionSource.SetException(e);
                  } else if(request is Request<List<string>> stringListRequest)
                  {
                     stringListRequest.TaskCompletionSource.SetException(e);
                  }
               }
            }
         }
         catch(Exception)
         {
            // Queue closed or other error
            if(!_running) break;
         }
      }
   }

   public JamdictLookupResult Lookup(string word, bool includeNames)
   {
      var tcs = new TaskCompletionSource<JamdictLookupResult>();

      JamdictLookupResult DoActualLookup(dynamic jamdict)
      {
         var lookupResult = jamdict.lookup(word, lookup_chars: false, lookup_ne: includeNames);

         // Convert to .NET types while holding GIL
         var entries = DictEntry.CreateFromPythonEntries(lookupResult.entries);
         var names = DictEntry.CreateFromPythonEntries(lookupResult.names);

         return new JamdictLookupResult(entries, names);
      }

      var request = new Request<JamdictLookupResult>(DoActualLookup, tcs);
      _queue.Add(request);

      return tcs.Task.Result;
   }

   public List<string> RunStringQuery(string sqlQuery)
   {
      List<string> PerformQuery(dynamic jamdict)
      {
         var result = new List<string>();

         var conn = jamdict.jmdict.ctx().conn;
         foreach(var batch in Dyn.Enumerate(conn.execute(sqlQuery)))
         {
            foreach(var row in Dyn.Enumerate(batch))
            {
               result.Add((string)row);
            }
         }

         return result;
      }

      var tcs = new TaskCompletionSource<List<string>>();
      var request = new Request<List<string>>(PerformQuery, tcs);
      _queue.Add(request);

      return tcs.Task.Result;
   }
}
