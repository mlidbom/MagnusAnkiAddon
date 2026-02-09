using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Storage;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Storage;

public class NoteSerializerRoundtripTests : CollectionUsingTest
{
    readonly NoteSerializer _serializer;

    public NoteSerializerRoundtripTests() : base(DataNeeded.All)
    {
        _serializer = GetService<NoteSerializer>();
    }

    [Fact]
    public void AllKanjiNotes_RoundtripToIdenticalJson()
    {
        var allKanji = NoteServices.Collection.Kanji.All();
        Assert.NotEmpty(allKanji);

        var failures = new List<string>();

        foreach (var kanji in allKanji)
        {
            var json = _serializer.Serialize(kanji);
            var roundtripped = _serializer.DeserializeKanji(json);
            var reJson = _serializer.Serialize(roundtripped);

            if (json != reJson)
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

        foreach (var vocab in allVocab)
        {
            var json = _serializer.Serialize(vocab);
            var roundtripped = _serializer.DeserializeVocab(json);
            var reJson = _serializer.Serialize(roundtripped);

            if (json != reJson)
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

        foreach (var sentence in allSentences)
        {
            var json = _serializer.Serialize(sentence);
            var roundtripped = _serializer.DeserializeSentence(json);
            var reJson = _serializer.Serialize(roundtripped);

            if (json != reJson)
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

        foreach (var kanji in allKanji)
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

        foreach (var vocab in allVocab)
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

        foreach (var sentence in allSentences)
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
        kanji.SetUserAnswer("custom answer");
        kanji.SetUserMnemonic("my mnemonic");
        kanji.SetRadicals("言, 弋, 工");
        kanji.AddUserSimilarMeaning("験");

        var json = _serializer.Serialize(kanji);
        var roundtripped = _serializer.DeserializeKanji(json);

        Assert.Equal(kanji.GetQuestion(), roundtripped.GetQuestion());
        Assert.Equal("custom answer", roundtripped.GetUserAnswer());
        Assert.Equal("my mnemonic", roundtripped.GetUserMnemonic());
        Assert.Contains("言", roundtripped.GetRadicals());
        Assert.Contains("験", roundtripped.GetUserSimilarMeaning());

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

    // The jas_note_id field is stored on the NoteId object, not in the fields dict,
    // so the original GetData() won't have it but the deserialized note will. Exclude from comparison.
    static readonly HashSet<string> FieldsExcludedFromComparison = [MyNoteFields.JasNoteId];

    static bool IsEffectivelyEmpty(string value) => string.IsNullOrEmpty(value) || value == "0";

    static string Truncate(string value, int maxLength) =>
        value.Length <= maxLength ? value : value.Substring(0, maxLength);

    static void AssertNoteDataFieldsMatch(NoteData original, NoteData roundtripped, string context)
    {
        Assert.Equal(original.Id, roundtripped.Id);

        Assert.Equal(
            original.Tags.OrderBy(t => t).ToList(),
            roundtripped.Tags.OrderBy(t => t).ToList());

        foreach (var kvp in roundtripped.Fields)
        {
            if (FieldsExcludedFromComparison.Contains(kvp.Key)) continue;

            var originalValue = original.Fields.TryGetValue(kvp.Key, out var v) ? v : string.Empty;
            if (IsEffectivelyEmpty(originalValue) && IsEffectivelyEmpty(kvp.Value)) continue;

            Assert.True(originalValue == kvp.Value,
                $"{context}: Field '{kvp.Key}' mismatch.\n  Original:     [{originalValue}]\n  Roundtripped: [{kvp.Value}]");
        }

        foreach (var kvp in original.Fields.Where(f => !string.IsNullOrEmpty(f.Value) && !FieldsExcludedFromComparison.Contains(f.Key)))
        {
            Assert.True(roundtripped.Fields.ContainsKey(kvp.Key),
                $"{context}: Original field '{kvp.Key}' with value [{kvp.Value}] missing from roundtripped data");
        }
    }
}
