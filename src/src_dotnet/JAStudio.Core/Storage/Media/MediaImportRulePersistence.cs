using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace JAStudio.Core.Storage.Media;

public class MediaImportRulePersistence
{
   static readonly JsonSerializerOptions JsonOptions = new()
                                                       {
                                                          WriteIndented = true,
                                                          PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                                                          DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingDefault,
                                                          Converters = { new JsonStringEnumConverter(), new SourceTagJsonConverter() }
                                                       };

   static string FilePath => Path.Combine(CoreApp.MetadataDir, "media-import-rules.json");

   public static PersistedImportRules Load()
   {
      var path = FilePath;
      if(!File.Exists(path)) return new PersistedImportRules();
      var json = File.ReadAllText(path);
      return JsonSerializer.Deserialize<PersistedImportRules>(json, JsonOptions) ?? new PersistedImportRules();
   }

   public static void Save(PersistedImportRules rules)
   {
      var path = FilePath;
      Directory.CreateDirectory(Path.GetDirectoryName(path)!);
      var json = JsonSerializer.Serialize(rules, JsonOptions);
      File.WriteAllText(path, json);
   }
}

public class PersistedImportRules
{
   public List<VocabImportRule> VocabRules { get; set; } = [];
   public List<SentenceImportRule> SentenceRules { get; set; } = [];
   public List<KanjiImportRule> KanjiRules { get; set; } = [];
}
