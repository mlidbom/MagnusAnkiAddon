using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Storage;
using Xunit;

namespace JAStudio.Core.Tests.Storage;

public class NoteSerializerRoundtripTests : Specification_using_a_collection
{
   readonly NoteSerializer _serializer;

   public NoteSerializerRoundtripTests() : base() => _serializer = GetService<NoteSerializer>();

   [Fact]
   public void AllKanjiNotes_RoundtripToIdenticalJson()
   {
      var allKanji = NoteServices.Collection.Kanji.All();
      Assert.NotEmpty(allKanji);

      var failures = new List<string>();

      foreach(var kanji in allKanji)
      {
         var json = _serializer.Serialize(kanji);
         var roundtripped = _serializer.DeserializeKanji(json);
         var reJson = _serializer.Serialize(roundtripped);

         if(json != reJson)
         {
            failures.Add($"Kanji '{kanji.GetQuestion()}': JSON differs after roundtrip");
         }
      }

      Assert.True(failures.Count == 0, $"Roundtrip failures:\n{string.Join("\n", failures)}");
   }

   [Fact]
   public void AllVocabNotes_RoundtripToIdenticalJson()
   {
      var allVocab = NoteServices.Collection.Vocab.All();
      Assert.NotEmpty(allVocab);

      var failures = new List<string>();

      foreach(var vocab in allVocab)
      {
         var json = _serializer.Serialize(vocab);
         var roundtripped = _serializer.DeserializeVocab(json);
         var reJson = _serializer.Serialize(roundtripped);

         if(json != reJson)
         {
            failures.Add($"Vocab '{vocab.GetQuestion()}': JSON differs after roundtrip");
         }
      }

      Assert.True(failures.Count == 0, $"Roundtrip failures:\n{string.Join("\n", failures)}");
   }

   [Fact]
   public void AllSentenceNotes_RoundtripToIdenticalJson()
   {
      var allSentences = NoteServices.Collection.Sentences.All();
      Assert.NotEmpty(allSentences);

      var failures = new List<string>();

      foreach(var sentence in allSentences)
      {
         var json = _serializer.Serialize(sentence);
         var roundtripped = _serializer.DeserializeSentence(json);
         var reJson = _serializer.Serialize(roundtripped);

         if(json != reJson)
         {
            failures.Add($"Sentence '{Truncate(sentence.GetQuestion(), 20)}': JSON differs after roundtrip");
         }
      }

      Assert.True(failures.Count == 0, $"Roundtrip failures:\n{string.Join("\n", failures)}");
   }

   [Fact]
   public void AllKanjiNotes_RoundtripThroughNoteData_PreservesAllFields()
   {
      var allKanji = NoteServices.Collection.Kanji.All();
      Assert.NotEmpty(allKanji);

      foreach(var kanji in allKanji)
      {
         var originalData = kanji.GetData();
         var json = _serializer.Serialize(kanji);
         var roundtripped = _serializer.DeserializeKanji(json);
         AssertNoteDataFieldsMatch(originalData, roundtripped.GetData(), $"Kanji '{kanji.GetQuestion()}'");
      }
   }

   [Fact]
   public void AllVocabNotes_RoundtripThroughNoteData_PreservesAllFields()
   {
      var allVocab = NoteServices.Collection.Vocab.All();
      Assert.NotEmpty(allVocab);

      foreach(var vocab in allVocab)
      {
         var originalData = vocab.GetData();
         var json = _serializer.Serialize(vocab);
         var roundtripped = _serializer.DeserializeVocab(json);
         AssertNoteDataFieldsMatch(originalData, roundtripped.GetData(), $"Vocab '{vocab.GetQuestion()}'");
      }
   }

   [Fact]
   public void AllSentenceNotes_RoundtripThroughNoteData_PreservesAllFields()
   {
      var allSentences = NoteServices.Collection.Sentences.All();
      Assert.NotEmpty(allSentences);

      foreach(var sentence in allSentences)
      {
         var originalData = sentence.GetData();
         var json = _serializer.Serialize(sentence);
         var roundtripped = _serializer.DeserializeSentence(json);
         AssertNoteDataFieldsMatch(originalData, roundtripped.GetData(), $"Sentence '{Truncate(sentence.GetQuestion(), 20)}'");
      }
   }

   [Fact]
   public void KanjiNote_WithRichData_RoundtripsCorrectly()
   {
      var kanji = CreateKanji("試", "test/try", "<primary>ため</primary>", "<primary>し</primary>");
      kanji.UserAnswer.Set("custom answer");
      kanji.UserMnemonic.Set("my mnemonic");
      kanji.SetRadicals("言, 弋, 工");
      kanji.AddUserSimilarMeaning("験");

      var json = _serializer.Serialize(kanji);
      var roundtripped = _serializer.DeserializeKanji(json);

      Assert.Equal(kanji.GetQuestion(), roundtripped.GetQuestion());
      Assert.Equal("custom answer", roundtripped.UserAnswer.Value);
      Assert.Equal("my mnemonic", roundtripped.UserMnemonic.Value);
      Assert.Contains("言", roundtripped.Radicals);
      Assert.Contains("験", roundtripped.UserSimilarMeaning);

      Assert.Equal(json, _serializer.Serialize(roundtripped));
   }

   [Fact]
   public void VocabNote_RoundtripsCorrectly()
   {
      var vocab = CreateVocab("試す", "to test", "ためす");

      var json = _serializer.Serialize(vocab);
      var roundtripped = _serializer.DeserializeVocab(json);

      Assert.Equal("試す", roundtripped.GetQuestion());
      Assert.Contains("ためす", roundtripped.GetReadings());
      Assert.Equal(json, _serializer.Serialize(roundtripped));
   }

   [Fact]
   public void SentenceNote_RoundtripsCorrectly()
   {
      var sentence = CreateTestSentence("テストの文です", "This is a test sentence.");

      var json = _serializer.Serialize(sentence);
      var roundtripped = _serializer.DeserializeSentence(json);

      Assert.Equal("テストの文です", roundtripped.GetQuestion());
      Assert.Equal(json, _serializer.Serialize(roundtripped));
   }

   static bool IsEffectivelyEmpty(string value) => string.IsNullOrEmpty(value) || value == "0";

   static string Truncate(string value, int maxLength) =>
      value.Length <= maxLength ? value : value.Substring(0, maxLength);

   static void AssertNoteDataFieldsMatch(NoteData original, NoteData roundtripped, string context)
   {
      Assert.Equal(original.Id, roundtripped.Id);

      Assert.Equal(
         original.Tags.OrderBy(t => t).ToList(),
         roundtripped.Tags.OrderBy(t => t).ToList());

      foreach(var kvp in roundtripped.Fields)
      {
         var originalValue = original.Fields.TryGetValue(kvp.Key, out var v) ? v : string.Empty;
         if(IsEffectivelyEmpty(originalValue) && IsEffectivelyEmpty(kvp.Value)) continue;

         Assert.True(originalValue == kvp.Value,
                     $"{context}: Field '{kvp.Key}' mismatch.\n  Original:     [{originalValue}]\n  Roundtripped: [{kvp.Value}]");
      }

      foreach(var kvp in original.Fields.Where(f => !string.IsNullOrEmpty(f.Value)))
      {
         Assert.True(roundtripped.Fields.ContainsKey(kvp.Key),
                     $"{context}: Original field '{kvp.Key}' with value [{kvp.Value}] missing from roundtripped data");
      }
   }

   [Fact]
   public void AllNotesData_RoundtripsToIdenticalJson()
   {
      var allData = new AllNotesData(
         NoteServices.Collection.Kanji.All(),
         NoteServices.Collection.Vocab.All(),
         NoteServices.Collection.Sentences.All());

      var json = _serializer.Serialize(allData);
      var roundtripped = _serializer.DeserializeAll(json);
      var reJson = _serializer.Serialize(roundtripped);

      Assert.Equal(json, reJson);
   }

   [Fact]
   public void AllNotesData_PreservesNoteCountsAfterRoundtrip()
   {
      var kanji = NoteServices.Collection.Kanji.All();
      var vocab = NoteServices.Collection.Vocab.All();
      var sentences = NoteServices.Collection.Sentences.All();

      var allData = new AllNotesData(kanji, vocab, sentences);
      var json = _serializer.Serialize(allData);
      var roundtripped = _serializer.DeserializeAll(json);

      Assert.Equal(kanji.Count, roundtripped.Kanji.Count);
      Assert.Equal(vocab.Count, roundtripped.Vocab.Count);
      Assert.Equal(sentences.Count, roundtripped.Sentences.Count);
   }

   [Fact]
   public void AllNotesData_PreservesAllFieldsAfterRoundtrip()
   {
      var allData = new AllNotesData(
         NoteServices.Collection.Kanji.All(),
         NoteServices.Collection.Vocab.All(),
         NoteServices.Collection.Sentences.All());

      var json = _serializer.Serialize(allData);
      var roundtripped = _serializer.DeserializeAll(json);

      for(var i = 0; i < allData.Kanji.Count; i++)
         AssertNoteDataFieldsMatch(allData.Kanji[i].GetData(), roundtripped.Kanji[i].GetData(), $"Kanji '{allData.Kanji[i].GetQuestion()}'");

      for(var i = 0; i < allData.Vocab.Count; i++)
         AssertNoteDataFieldsMatch(allData.Vocab[i].GetData(), roundtripped.Vocab[i].GetData(), $"Vocab '{allData.Vocab[i].GetQuestion()}'");

      for(var i = 0; i < allData.Sentences.Count; i++)
         AssertNoteDataFieldsMatch(allData.Sentences[i].GetData(), roundtripped.Sentences[i].GetData(), $"Sentence '{Truncate(allData.Sentences[i].GetQuestion(), 20)}'");
   }
}
