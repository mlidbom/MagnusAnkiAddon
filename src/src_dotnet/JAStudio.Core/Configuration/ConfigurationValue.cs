using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace JAStudio.Core.Configuration;

public class ConfigurationValue
{
   readonly TemporaryServiceCollection _services;
   internal ConfigurationValue(TemporaryServiceCollection services) => _services = services;

   static Dictionary<string, object>? _configDict;
   static Action<string>? _updateCallback;
   internal static Dictionary<string, string>? StaticReadingsMappings;

   public static void InitPreviewForTesting()
   {
      if(_configDict != null) return;
      InitJson("{}", s => {});
      StaticReadingsMappings = new Dictionary<string, string>();
   }

   public static void InitJson(string json, Action<string> updateCallback)
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
      if(App.IsTesting)
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
      if(!App.IsTesting && _updateCallback != null && _configDict != null)
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
}

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

      var configDict = ConfigurationValue.GetConfigDict();

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

      ConfigurationValue.GetConfigDict()[Name] = value!;

      ToggleFeature();

      ConfigurationValue.WriteConfigDict();

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