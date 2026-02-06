using System;
using System.Collections.Generic;
using JAStudio.Core.TestUtils;
using Newtonsoft.Json;

namespace JAStudio.Core.Configuration;

static class ConfigurationManager
{
   static Dictionary<string, object>? _configDict;
   static Action<string>? _updateCallback;
   internal static Dictionary<string, string>? StaticReadingsMappings;

   public static void InitForTesting()
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
      if(TestEnvDetector.IsTesting)
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
      if(!TestEnvDetector.IsTesting && _updateCallback != null && _configDict != null)
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
