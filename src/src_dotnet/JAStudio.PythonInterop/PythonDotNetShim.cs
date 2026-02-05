using System;
using System.Collections.Generic;

namespace JAStudio.PythonInterop;

/// <summary>
/// Bridge utilities for converting Python objects to .NET types.
/// Isolates Python.NET conversion complexity from domain code.
/// </summary>
public static class PythonDotNetShim
{
    /// <summary>
    /// Converts a Python dictionary to a .NET Dictionary&lt;string, object&gt;.
    /// </summary>
    /// <param name="pythonDict">Python dictionary object</param>
    /// <returns>.NET Dictionary with string keys and object values</returns>
    public static Dictionary<string, object> ToDotNetDict(dynamic pythonDict)
    {
        var result = new Dictionary<string, object>();
        
        foreach (var key in pythonDict.Keys)
        {
            result[key.ToString()] = pythonDict[key];
        }
        
        return result;
    }
    
    /// <summary>
    /// Converts a Python callable to a .NET Action&lt;Dictionary&lt;string, object&gt;&gt;.
    /// </summary>
    /// <param name="pythonCallable">Python callable that accepts a dictionary</param>
    /// <returns>.NET Action delegate</returns>
    public static Action<Dictionary<string, object>> ToDotNetDictAction(dynamic pythonCallable)
    {
        return (dict) =>
        {
            // Convert .NET Dictionary back to Python dict for the callback
            dynamic pythonDict = new Python.Runtime.PyDict();
            foreach (var kvp in dict)
            {
                pythonDict[kvp.Key] = kvp.Value;
            }
            pythonCallable(pythonDict);
        };
    }
}
