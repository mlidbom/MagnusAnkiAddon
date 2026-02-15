using System;
using System.Collections.Generic;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.PythonInterop;

public static class PythonDotNetShim
{
   public static class StringStringDict
   {
      public static Dictionary<string, string> ToDotNet(dynamic pythonDict) => PythonEnvironment.Use(() =>
      {
         var result = new Dictionary<string, string>();

         foreach(var key in pythonDict.keys())
         {
            result[(string)key] = (string)pythonDict[key];
         }

         return result;
      });

      public static dynamic ToPython(IReadOnlyDictionary<string, string> dict) => PythonEnvironment.Use(() =>
      {
         dynamic pythonDict = new PyDict();

         foreach(var kvp in dict)
            pythonDict[kvp.Key] = new PyString(kvp.Value);
         return pythonDict;
      });
   }

   public static class StringList
   {
      public static List<string> ToDotNet(dynamic pythonList) => PythonEnvironment.Use(() =>
      {
         var result = new List<string>();

         foreach(var item in pythonList)
         {
            result.Add((string)item);
         }

         return result;
      });

      public static dynamic ToPython(IReadOnlyList<string> list) => PythonEnvironment.Use(() =>
      {
         dynamic pythonList = new PyList();

         foreach(var item in list)
         {
            pythonList.Append(new PyString(item));
         }

         return pythonList;
      });
   }

   public static class Action
   {
      public static Action<T> ToDotNet<T>(dynamic action)
      {
         return it => PythonEnvironment.Use(() => action(it));
      }
   }

   public static class LongList
   {
      public static List<long> ToDotNet(dynamic pythonList) => PythonEnvironment.Use(() =>
      {
         var result = new List<long>();

         foreach(var item in pythonList)
         {
            result.Add((long)item);
         }

         return result;
      });

      public static dynamic ToPython(IReadOnlyList<long> items) => PythonEnvironment.Use(() =>
      {
         dynamic pyList = new PyList();

         foreach(var item in items)
         {
            pyList.append(new PyInt(item));
         }

         return pyList;
      });
   }
}
