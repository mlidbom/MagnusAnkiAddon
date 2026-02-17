using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.NoteFields.AutoSaveWrappers;
using JAStudio.Core.SysUtils.Json;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

class RelatedVocabDataSerializer : IObjectSerializer<RelatedVocabData>
{
   readonly string _emptyObjectJson;

   public RelatedVocabDataSerializer() => _emptyObjectJson = Serialize(Deserialize(string.Empty));

   public RelatedVocabData Deserialize(string serialized)
   {
      if(string.IsNullOrEmpty(serialized))
      {
         return new RelatedVocabData(
            string.Empty,
            new ValueWrapper<string>(string.Empty),
            [],
            [],
            [],
            [],
            []
         );
      }

      using var doc = JsonDocument.Parse(serialized);
      var reader = new JsonReader(doc.RootElement);

      return new RelatedVocabData(
         reader.GetString("ergative_twin", string.Empty),
         new ValueWrapper<string>(reader.GetString("derived_from", string.Empty)),
         reader.GetStringSet("perfect_synonyms", []),
         reader.GetStringSet("synonyms", []),
         reader.GetStringSet("antonyms", []),
         reader.GetStringSet("confused_with", []),
         reader.GetStringSet("see_also", [])
      );
   }

   public string Serialize(RelatedVocabData instance)
   {
      var dict = new Dictionary<string, object>();

      if(!string.IsNullOrEmpty(instance.ErgativeTwin))
         dict["ergative_twin"] = instance.ErgativeTwin;

      if(!string.IsNullOrEmpty(instance.DerivedFrom.Get()))
         dict["derived_from"] = instance.DerivedFrom.Get();

      if(instance.Synonyms.Any())
         dict["synonyms"] = instance.Synonyms.OrderBy(s => s).ToList();

      if(instance.PerfectSynonyms.Any())
         dict["perfect_synonyms"] = instance.PerfectSynonyms.OrderBy(s => s).ToList();

      if(instance.Antonyms.Any())
         dict["antonyms"] = instance.Antonyms.OrderBy(s => s).ToList();

      if(instance.ConfusedWith.Any())
         dict["confused_with"] = instance.ConfusedWith.OrderBy(s => s).ToList();

      if(instance.SeeAlso.Any())
         dict["see_also"] = instance.SeeAlso.OrderBy(s => s).ToList();

      var json = JsonHelper.DictToJson(dict);
      return json != _emptyObjectJson ? json : string.Empty;
   }
}
