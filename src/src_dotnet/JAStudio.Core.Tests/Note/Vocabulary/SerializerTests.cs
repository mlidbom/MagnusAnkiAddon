using System.Collections.Generic;
using JAStudio.Core.Note.NoteFields.AutoSaveWrappers;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Note.Vocabulary.RelatedVocab;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests.Note.Vocabulary;

public class RelatedVocabDataSerializerTests : TestStartingWithEmptyCollection
{
   readonly RelatedVocabDataSerializer _serializer = RelatedVocabData.Serializer();

   [Fact]
   public void EmptyObjectSerializesToEmptyString()
   {
      var emptyData = new RelatedVocabData(
         ergativeTwin: "",
         derivedFrom: new ValueWrapper<string>(""),
         perfectSynonyms: [],
         similar: [],
         antonyms: [],
         confusedWith: [],
         seeAlso: []
      );

      var result = _serializer.Serialize(emptyData);

      Assert.Equal("", result);
   }

   [Fact]
   public void DeserializeEmptyStringReturnsEmptyData()
   {
      var result = _serializer.Deserialize("");

      Assert.Equal("", result.ErgativeTwin);
      Assert.Equal("", result.DerivedFrom.Get());
      Assert.Empty(result.PerfectSynonyms);
      Assert.Empty(result.Synonyms);
      Assert.Empty(result.Antonyms);
      Assert.Empty(result.ConfusedWith);
      Assert.Empty(result.SeeAlso);
   }

   [Fact]
   public void RoundtripWithDataPreservesAllFields()
   {
      var original = new RelatedVocabData(
         ergativeTwin: "開く",
         derivedFrom: new ValueWrapper<string>("開ける"),
         perfectSynonyms: ["完璧", "完全"],
         similar: ["似ている", "同様"],
         antonyms: ["閉じる", "閉める"],
         confusedWith: ["明く"],
         seeAlso: ["開放", "開始"]
      );

      var serialized = _serializer.Serialize(original);
      var deserialized = _serializer.Deserialize(serialized);

      Assert.Equal("開く", deserialized.ErgativeTwin);
      Assert.Equal("開ける", deserialized.DerivedFrom.Get());
      Assert.Equal(["完璧", "完全"], deserialized.PerfectSynonyms);
      Assert.Equal(["似ている", "同様"], deserialized.Synonyms);
      Assert.Equal(["閉じる", "閉める"], deserialized.Antonyms);
      Assert.Equal(["明く"], deserialized.ConfusedWith);
      Assert.Equal(["開放", "開始"], deserialized.SeeAlso);
   }
}

public class VocabNoteMatchingRulesSerializerTests : TestStartingWithEmptyCollection
{
   readonly VocabNoteMatchingRulesSerializer _serializer = new();

   [Fact]
   public void EmptyObjectSerializesToEmptyString()
   {
      var emptyData = new VocabNoteMatchingRulesData(
         surfaceIsNot: [],
         prefixIsNot: [],
         suffixIsNot: [],
         requiredPrefix: [],
         yieldToSurface: []
      );

      var result = _serializer.Serialize(emptyData);

      Assert.Equal("", result);
   }

   [Fact]
   public void RoundtripWithDataPreservesAllFields()
   {
      var original = new VocabNoteMatchingRulesData(
         surfaceIsNot: ["surface1", "surface2"],
         prefixIsNot: ["prefix1"],
         suffixIsNot: ["suffix1", "suffix2", "suffix3"],
         requiredPrefix: ["req1"],
         yieldToSurface: ["yield1", "yield2"]
      );

      var serialized = _serializer.Serialize(original);
      var deserialized = _serializer.Deserialize(serialized);

      Assert.Equal(["surface1", "surface2"], deserialized.SurfaceIsNot);
      Assert.Equal(["prefix1"], deserialized.PrefixIsNot);
      Assert.Equal(["suffix1", "suffix2", "suffix3"], deserialized.SuffixIsNot);
      Assert.Equal(["req1"], deserialized.RequiredPrefix);
      Assert.Equal(["yield1", "yield2"], deserialized.YieldToSurface);
   }
}
