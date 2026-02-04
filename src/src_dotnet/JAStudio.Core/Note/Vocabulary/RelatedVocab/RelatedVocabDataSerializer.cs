using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class RelatedVocabDataSerializer : IObjectSerializer<RelatedVocabData>
{
    private string _emptyObjectJson = string.Empty;

    public RelatedVocabDataSerializer()
    {
        _emptyObjectJson = Serialize(Deserialize(string.Empty));
    }

    public RelatedVocabData Deserialize(string serialized)
    {
        if (string.IsNullOrEmpty(serialized))
        {
            return new RelatedVocabData(
                string.Empty,
                new ValueWrapper<string>(string.Empty),
                new HashSet<string>(),
                new HashSet<string>(),
                new HashSet<string>(),
                new HashSet<string>(),
                new HashSet<string>()
            );
        }

        using var doc = JsonDocument.Parse(serialized);
        var root = doc.RootElement;

        return new RelatedVocabData(
            GetString(root, "ergative_twin", string.Empty),
            new ValueWrapper<string>(GetString(root, "derived_from", string.Empty)),
            GetStringSet(root, "perfect_synonyms"),
            GetStringSet(root, "synonyms"),
            GetStringSet(root, "antonyms"),
            GetStringSet(root, "confused_with"),
            GetStringSet(root, "see_also")
        );
    }

    public string Serialize(RelatedVocabData instance)
    {
        var dict = new Dictionary<string, object>();

        if (!string.IsNullOrEmpty(instance.ErgativeTwin))
            dict["ergative_twin"] = instance.ErgativeTwin;
        
        if (!string.IsNullOrEmpty(instance.DerivedFrom.Get()))
            dict["derived_from"] = instance.DerivedFrom.Get();
        
        if (instance.Synonyms.Any())
            dict["synonyms"] = instance.Synonyms.ToList();
        
        if (instance.PerfectSynonyms.Any())
            dict["perfect_synonyms"] = instance.PerfectSynonyms.ToList();
        
        if (instance.Antonyms.Any())
            dict["antonyms"] = instance.Antonyms.ToList();
        
        if (instance.ConfusedWith.Any())
            dict["confused_with"] = instance.ConfusedWith.ToList();
        
        if (instance.SeeAlso.Any())
            dict["see_also"] = instance.SeeAlso.ToList();

        var json = JsonSerializer.Serialize(dict);
        return json != _emptyObjectJson ? json : string.Empty;
    }

    private static string GetString(JsonElement element, string propertyName, string defaultValue)
    {
        return element.TryGetProperty(propertyName, out var property) && property.ValueKind == JsonValueKind.String
            ? property.GetString() ?? defaultValue
            : defaultValue;
    }

    private static HashSet<string> GetStringSet(JsonElement element, string propertyName)
    {
        if (!element.TryGetProperty(propertyName, out var property) || property.ValueKind != JsonValueKind.Array)
            return new HashSet<string>();

        return property.EnumerateArray()
            .Where(item => item.ValueKind == JsonValueKind.String)
            .Select(item => item.GetString()!)
            .ToHashSet();
    }
}
