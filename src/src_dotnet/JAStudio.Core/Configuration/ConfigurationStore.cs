using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using JAStudio.Core.TestUtils;
using Newtonsoft.Json;

namespace JAStudio.Core.Configuration;

public class ConfigurationStore
{
   static Dictionary<string, object>? _configDict;
   static Action<string>? _updateCallback;

   public static void InitForTesting()
   {
      if(_configDict != null) return;
      InitJson("{}", s => {});
      _readingsMappingsOverride = new Dictionary<string, string>();
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

   // --- Readings mappings ---

   static Dictionary<string, string>? _readingsMappingsOverride;

   public static Dictionary<string, string> GetReadingsMappings()
   {
      return _readingsMappingsOverride ?? ReadReadingsMappingsFromFile();
   }

   public static void SetReadingsMappingsForTesting(string mappings)
   {
      _readingsMappingsOverride = ParseMappingsFromString(mappings);
   }

   public static void SaveMappings(string mappings)
   {
      File.WriteAllText(MappingsFilePath(), mappings);
      _readingsMappingsOverride = null;
   }

   public static string ReadReadingsMappingsFile() => File.ReadAllText(MappingsFilePath());

   static Dictionary<string, string> ReadReadingsMappingsFromFile() => ParseMappingsFromString(ReadReadingsMappingsFile());

   static Dictionary<string, string> ParseMappingsFromString(string mappingsString)
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

   static string MappingsFilePath() => Path.Combine(App.UserFilesDir, "readings_mappings.txt");
}
