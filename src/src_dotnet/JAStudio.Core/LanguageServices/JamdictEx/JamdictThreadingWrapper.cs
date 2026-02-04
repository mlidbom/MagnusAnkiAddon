using System;
using System.Collections.Generic;
using System.Data;
using System.Threading;
using System.Threading.Channels;
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

public class JamdictThreadingWrapper
{
    private readonly Channel<object> _queue;
    private readonly Thread _thread;
    private bool _running;
    private dynamic? _jamdict;

    public JamdictThreadingWrapper()
    {
        _queue = Channel.CreateUnbounded<object>();
        _running = true;
        _thread = new Thread(Worker) { IsBackground = true };
        _thread.Start();
    }

    private static dynamic CreateJamdict()
    {
        return PythonEnvironment.Use(() =>
        {
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
        });
    }

    private dynamic GetJamdict()
    {
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
                var request = _queue.Reader.ReadAsync().AsTask().Result;
                
                PythonEnvironment.Use(() =>
                {
                    try
                    {
                        if (request is Request<dynamic> dynamicRequest)
                        {
                            var result = dynamicRequest.Func(GetJamdict());
                            dynamicRequest.TaskCompletionSource.SetResult(result);
                        }
                        else if (request is Request<List<string>> stringListRequest)
                        {
                            var result = stringListRequest.Func(GetJamdict());
                            stringListRequest.TaskCompletionSource.SetResult(result);
                        }
                    }
                    catch (Exception e)
                    {
                        if (request is Request<dynamic> dynamicRequest)
                        {
                            dynamicRequest.TaskCompletionSource.SetException(e);
                        }
                        else if (request is Request<List<string>> stringListRequest)
                        {
                            stringListRequest.TaskCompletionSource.SetException(e);
                        }
                    }
                });
            }
            catch (Exception)
            {
                // Channel closed or other error
                if (!_running) break;
            }
        }
    }

    public dynamic Lookup(string word, bool includeNames)
    {
        var tcs = new TaskCompletionSource<dynamic>();

        dynamic DoActualLookup(dynamic jamdict)
        {
            return jamdict.lookup(word, lookup_chars: false, lookup_ne: includeNames);
        }

        var request = new Request<dynamic>(DoActualLookup, tcs);
        _queue.Writer.TryWrite(request);
        
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
        _queue.Writer.TryWrite(request);
        
        return tcs.Task.Result;
    }

    public void Stop()
    {
        _running = false;
        _queue.Writer.Complete();
    }
}
