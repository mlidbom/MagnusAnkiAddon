using System;
using System.Collections.Generic;
using JAStudio.PythonInterop.Utilities;

namespace JAStudio.PythonInterop;

/// <summary>
/// Bridge utilities for converting Python objects to .NET types.
/// Isolates Python.NET conversion complexity from domain code.
/// </summary>
public static class PythonDotNetShim
{
   public static class ConfigDict
   {
      public static Dictionary<string, string> ToDotNetDict(dynamic pythonDict)
      {
         return PythonEnvironment.Use(() =>
         {
            var result = new Dictionary<string, string>();

            foreach(var key in pythonDict.keys())
            {
               result[(string)key] = (string)pythonDict[key];
            }

            return result;
         });
      }

      public static Action<Dictionary<string, string>> ToDotNetDictAction(dynamic pythonCallable)
      {
         return dict =>
         {
            PythonEnvironment.Use(() =>
            {
               dynamic pythonDict = new Python.Runtime.PyDict();
               {
                  foreach(var kvp in dict)
                     pythonDict[kvp.Key] = new Python.Runtime.PyString(kvp.Value);
               }

               pythonCallable(pythonDict);
            });
         };
      }
   }
}
