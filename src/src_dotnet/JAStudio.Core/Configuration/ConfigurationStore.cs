using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using JAStudio.Core.TestUtils;
using Newtonsoft.Json;

namespace JAStudio.Core.Configuration;

public class ConfigurationStore
{
   readonly TemporaryServiceCollection _services;
   internal ConfigurationStore(TemporaryServiceCollection services) => _services = services;

   Dictionary<string, object>? _configDict;
   Action<string>? _updateCallback;

   public void InitForTesting()
   {
      if(_configDict != null) return;
      InitJson("{}", s => {});
      _readingsMappingsOverride = new Dictionary<string, string>();
   }

   public void SetReadingsMappingsForTesting(string mappings)
   {
      _readingsMappingsOverride = ParseMappingsFromString(mappings);
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
      return _config ??= new JapaneseConfig();
   }

   // --- Readings mappings ---

   Dictionary<string, string>? _readingsMappingsOverride;

   public Dictionary<string, string> GetReadingsMappings() => _readingsMappingsOverride ?? ReadReadingsMappingsFromFile();

   public void SaveMappings(string mappings)
   {
      File.WriteAllText(MappingsFilePath(), mappings);
      _readingsMappingsOverride = null;
   }

   public string ReadReadingsMappingsFile() => File.ReadAllText(MappingsFilePath());

   Dictionary<string, string> ReadReadingsMappingsFromFile() => ParseMappingsFromString(ReadReadingsMappingsFile());

   Dictionary<string, string> ParseMappingsFromString(string mappingsString)
   {
      string ParseValuePart(string valuePart)
      {
         if(valuePart.Contains("<read>"))
         {
            return valuePart;
         }

         if(valuePart.Contains(":"))
         {
            var parts = valuePart.Split([':'], 2);
            return $"<read>{parts[0].Trim()}</read>{parts[1]}";
         }

         return $"<read>{valuePart}</read>";
      }

      return mappingsString.Trim().Split('\n')
                           .Where(line => line.Contains(":"))
                           .Select(line => line.Split([':'], 2))
                           .ToDictionary(
                               parts => parts[0].Trim(),
                               parts => ParseValuePart(parts[1].Trim())
                            );
   }

   string MappingsFilePath() => Path.Combine(App.UserFilesDir, "readings_mappings.txt");
}
