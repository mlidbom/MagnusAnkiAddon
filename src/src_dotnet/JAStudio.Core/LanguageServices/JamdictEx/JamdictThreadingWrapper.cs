using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.Core.LanguageServices.JamdictEx;

internal class Request<T>
{
    public Func<dynamic, T> Func { get; }
    public TaskCompletionSource<T> TaskCompletionSource { get; }

    public Request(Func<dynamic, T> func, TaskCompletionSource<T> taskCompletionSource)
    {
        Func = func;
        TaskCompletionSource = taskCompletionSource;
    }
}

public class JamdictLookupResult
{
    public List<DictEntry> Entries { get; }
    public List<DictEntry> Names { get; }

    public JamdictLookupResult(List<DictEntry> entries, List<DictEntry> names)
    {
        Entries = entries;
        Names = names;
    }
}

public class JamdictThreadingWrapper
{
    private readonly BlockingCollection<object> _queue;
    private readonly Thread _thread;
    private bool _running;
    private dynamic? _jamdict;

    public JamdictThreadingWrapper()
    {
        _queue = new BlockingCollection<object>();
        _running = true;
        _thread = new Thread(Worker) { IsBackground = true };
        _thread.Start();
    }

    private static dynamic CreateJamdict()
    {
        // NOTE: Caller must already hold the GIL
        dynamic jamdict_module = Py.Import("jamdict");
        
        bool memoryMode = App.Config().LoadJamdictDbIntoMemory.GetValue() && !App.IsTesting;
        
        if (memoryMode)
        {
            return jamdict_module.Jamdict(memory_mode: true);
        }
        else
        {
            return jamdict_module.Jamdict(reuse_ctx: true);
        }
    }

    private dynamic GetJamdict()
    {
        // NOTE: Caller must already hold the GIL
        if (_jamdict == null)
        {
            _jamdict = CreateJamdict();
        }
        return _jamdict;
    }

    private void Worker()
    {
        while (_running)
        {
            try
            {
                // Wait for request WITHOUT holding GIL
                var request = _queue.Take();
                
                // Acquire GIL only for processing this request
                using (PythonEnvironment.LockGil())
                {
                    try
                    {
                        if (request is Request<JamdictLookupResult> lookupRequest)
                        {
                            var result = lookupRequest.Func(GetJamdict());
                            lookupRequest.TaskCompletionSource.SetResult(result);
                        }
                        else if (request is Request<List<string>> stringListRequest)
                        {
                            var result = stringListRequest.Func(GetJamdict());
                            stringListRequest.TaskCompletionSource.SetResult(result);
                        }
                    }
                    catch (Exception e)
                    {
                        if (request is Request<JamdictLookupResult> lookupRequest)
                        {
                            lookupRequest.TaskCompletionSource.SetException(e);
                        }
                        else if (request is Request<List<string>> stringListRequest)
                        {
                            stringListRequest.TaskCompletionSource.SetException(e);
                        }
                    }
                }
            }
            catch (Exception)
            {
                // Queue closed or other error
                if (!_running) break;
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
            foreach (var batch in Dyn.Enumerate(conn.execute(sqlQuery)))
            {
                foreach (var row in Dyn.Enumerate(batch))
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
