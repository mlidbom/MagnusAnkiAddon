using System;
using System.Collections.Generic;

namespace JAStudio.Core.Configuration;

public class ConfigurationValue<T>
{
   T _value;
   readonly Dictionary<string, object> _configDict;
   readonly List<Action<T>> _changeCallbacks = [];

   public string Title { get; }
   public string Name { get; }

   public ConfigurationValue(string name, string title, T defaultValue, Func<object, T> converter, Dictionary<string, object> configDict)
   {
      Title = title;
      Name = name;
      _configDict = configDict;

      _value = configDict.TryGetValue(name, out var value)
                  ? converter(value)
                  : defaultValue;
   }

   public T GetValue() => _value;

   public void SetValue(T value)
   {
      _value = value;

      _configDict[Name] = value!;

      foreach(var callback in _changeCallbacks)
      {
         callback(GetValue());
      }
   }

   public void OnChange(Action<T> callback)
   {
      _changeCallbacks.Add(callback);
   }
}
