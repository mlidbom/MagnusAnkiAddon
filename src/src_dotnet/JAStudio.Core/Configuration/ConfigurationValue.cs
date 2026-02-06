using System;
using System.Collections.Generic;

namespace JAStudio.Core.Configuration;

public class ConfigurationValue<T>
{
   T _value;
   readonly List<Action<T>> _changeCallbacks = [];

   public string Title { get; }
   public Action<T>? FeatureToggler { get; }
   public string Name { get; }

   public ConfigurationValue(string name, string title, T defaultValue, Func<object, T> converter, Action<T>? featureToggler = null)
   {
      Title = title;
      FeatureToggler = featureToggler;
      Name = name;

      var configDict = App.GetConfigDict();

      _value = configDict.TryGetValue(name, out var value)
                  ? converter(value)
                  : defaultValue;

      if(FeatureToggler != null)
      {
         App.AddInitHook(ToggleFeature);
      }
   }

   public T GetValue() => _value;

   public void SetValue(T value)
   {
      _value = value;

      App.GetConfigDict()[Name] = value!;

      ToggleFeature();

      App.WriteConfigDict();

      foreach(var callback in _changeCallbacks)
      {
         callback(GetValue());
      }
   }

   public void OnChange(Action<T> callback)
   {
      _changeCallbacks.Add(callback);
   }

   public void ToggleFeature()
   {
      FeatureToggler?.Invoke(_value);
   }
}