using System;
using System.Collections.Generic;
using JAStudio.Core.TestUtils;
using Newtonsoft.Json;

namespace JAStudio.Core.Configuration;

public class ConfigurationStore
{
   readonly IReadingsMappingsSource _mappingsSource;

   internal ConfigurationStore(IReadingsMappingsSource mappingsSource)
   {
      _mappingsSource = mappingsSource;
   }

   Dictionary<string, object>? _configDict;
   Action<string>? _updateCallback;

   public void InitForTesting()
   {
      if(_configDict != null) return;
      InitJson("{}", _ => {});
   }

   public void InitJson(string json, Action<string> updateCallback)
   {
      if(_configDict != null)
      {
         throw new InvalidOperationException("Configuration dict already initialized");
      }

      _configDict = JsonConvert.DeserializeObject<Dictionary<string, object>>(json);
      _updateCallback = updateCallback;
   }

   internal Dictionary<string, object> GetConfigDict() => _configDict ?? throw new InvalidOperationException("Configuration dict not initialized");

   internal void WriteConfigDict()
   {
      if(!TestEnvDetector.IsTesting && _updateCallback != null && _configDict != null)
      {
         var json = JsonConvert.SerializeObject(_configDict, Formatting.None);
         _updateCallback(json);
      }
   }

   JapaneseConfig? _config;

   public JapaneseConfig Config()
   {
      return _config ??= new JapaneseConfig(this);
   }

   // --- Readings mappings ---

   public Dictionary<string, string> GetReadingsMappings() => _mappingsSource.GetMappings();

   public void SaveMappings(string mappings) => _mappingsSource.SaveMappings(mappings);

   public string ReadReadingsMappingsFile() => _mappingsSource.ReadRawMappings();
}
