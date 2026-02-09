using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using JAStudio.Core.Note;
using JAStudio.Core.Storage.Converters;
using JAStudio.Core.Storage.Dto;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Note;

public class DtoRoundtripTests : CollectionUsingTest
{
    static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
    };

    public DtoRoundtripTests() : base(DataNeeded.All)
    {
    }

    [Fact]
    public void AllKanjiNotes_RoundtripToIdenticalJson()
    {
        var allKanji = NoteServices.Collection.Kanji.All();
        Assert.NotEmpty(allKanji);

        var failures = new List<string>();

        foreach (var kanji in allKanji)
        {
            var dto = KanjiNoteConverter.ToDto(kanji);
            var json = JsonSerializer.Serialize(dto, JsonOptions);
            var deserialized = JsonSerializer.Deserialize<KanjiNoteDto>(json, JsonOptions)!;
            var reJson = JsonSerializer.Serialize(deserialized, JsonOptions);

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
            var dto = VocabNoteConverter.ToDto(vocab);
            var json = JsonSerializer.Serialize(dto, JsonOptions);
            var deserialized = JsonSerializer.Deserialize<VocabNoteDto>(json, JsonOptions)!;
            var reJson = JsonSerializer.Serialize(deserialized, JsonOptions);

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
            var dto = SentenceNoteConverter.ToDto(sentence);
            var json = JsonSerializer.Serialize(dto, JsonOptions);
            var deserialized = JsonSerializer.Deserialize<SentenceNoteDto>(json, JsonOptions)!;
            var reJson = JsonSerializer.Serialize(deserialized, JsonOptions);

            if (json != reJson)
            {
                failures.Add($"Sentence '{sentence.GetQuestion().Substring(0, System.Math.Min(20, sentence.GetQuestion().Length))}': JSON differs after roundtrip");
            }
        }

        Assert.True(failures.Count == 0, $"Roundtrip failures:\n{string.Join("\n", failures)}");
    }

    [Fact]
    public void KanjiNote_RoundtripThroughNoteData_PreservesAllFields()
    {
        var kanji = NoteServices.Collection.Kanji.All().First();
        var originalData = kanji.GetData();

        var dto = KanjiNoteConverter.ToDto(kanji);
        var roundtrippedData = KanjiNoteConverter.FromDto(dto);

        AssertNoteDataFieldsMatch(originalData, roundtrippedData, $"Kanji '{kanji.GetQuestion()}'");
    }

    [Fact]
    public void VocabNote_RoundtripThroughNoteData_PreservesAllFields()
    {
        var vocab = NoteServices.Collection.Vocab.All().First();
        var originalData = vocab.GetData();

        var dto = VocabNoteConverter.ToDto(vocab);
        var roundtrippedData = VocabNoteConverter.FromDto(dto);

        AssertNoteDataFieldsMatch(originalData, roundtrippedData, $"Vocab '{vocab.GetQuestion()}'");
    }

    [Fact]
    public void SentenceNote_RoundtripThroughNoteData_PreservesAllFields()
    {
        var sentence = NoteServices.Collection.Sentences.All().First();
        var originalData = sentence.GetData();

        var dto = SentenceNoteConverter.ToDto(sentence);
        var roundtrippedData = SentenceNoteConverter.FromDto(dto);

        AssertNoteDataFieldsMatch(originalData, roundtrippedData, $"Sentence '{sentence.GetQuestion()}'");
    }

    [Fact]
    public void AllKanjiNotes_RoundtripThroughNoteData_PreservesAllFields()
    {
        var allKanji = NoteServices.Collection.Kanji.All();
        Assert.NotEmpty(allKanji);

        foreach (var kanji in allKanji)
        {
            var originalData = kanji.GetData();
            var dto = KanjiNoteConverter.ToDto(kanji);
            var roundtrippedData = KanjiNoteConverter.FromDto(dto);
            AssertNoteDataFieldsMatch(originalData, roundtrippedData, $"Kanji '{kanji.GetQuestion()}'");
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
            var dto = VocabNoteConverter.ToDto(vocab);
            var roundtrippedData = VocabNoteConverter.FromDto(dto);
            AssertNoteDataFieldsMatch(originalData, roundtrippedData, $"Vocab '{vocab.GetQuestion()}'");
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
            var dto = SentenceNoteConverter.ToDto(sentence);
            var roundtrippedData = SentenceNoteConverter.FromDto(dto);
            AssertNoteDataFieldsMatch(originalData, roundtrippedData, $"Sentence '{sentence.GetQuestion()}'");
        }
    }

    [Fact]
    public void KanjiNote_WithRichData_RoundtripsJsonCorrectly()
    {
        // Create a kanji with various populated fields
        var kanji = CreateKanji("試", "test/try", "<primary>ため</primary>", "<primary>し</primary>");
        kanji.SetUserAnswer("custom answer");
        kanji.SetUserMnemonic("my mnemonic");
        kanji.SetRadicals("言, 弋, 工");
        kanji.AddUserSimilarMeaning("験");

        var dto = KanjiNoteConverter.ToDto(kanji);
        var json = JsonSerializer.Serialize(dto, JsonOptions);
        var deserialized = JsonSerializer.Deserialize<KanjiNoteDto>(json, JsonOptions)!;
        var reJson = JsonSerializer.Serialize(deserialized, JsonOptions);

        Assert.Equal(json, reJson);
        Assert.Equal("試", deserialized.Kanji);
        Assert.Equal("custom answer", deserialized.UserAnswer);
        Assert.Equal("my mnemonic", deserialized.UserMnemonic);
        Assert.Contains("言", deserialized.Radicals);
        Assert.Contains("験", deserialized.SimilarMeaning);
    }

    [Fact]
    public void VocabNote_WithMatchingRulesAndRelated_RoundtripsJsonCorrectly()
    {
        var vocab = CreateVocab("試す", "to test", "ためす");

        var dto = VocabNoteConverter.ToDto(vocab);
        var json = JsonSerializer.Serialize(dto, JsonOptions);
        var deserialized = JsonSerializer.Deserialize<VocabNoteDto>(json, JsonOptions)!;
        var reJson = JsonSerializer.Serialize(deserialized, JsonOptions);

        Assert.Equal(json, reJson);
        Assert.Equal("試す", deserialized.Question);
        Assert.Contains("ためす", deserialized.Readings);
    }

    [Fact]
    public void SentenceNote_WithParsingAndConfiguration_RoundtripsJsonCorrectly()
    {
        var sentence = CreateTestSentence("テストの文です", "This is a test sentence.");

        var dto = SentenceNoteConverter.ToDto(sentence);
        var json = JsonSerializer.Serialize(dto, JsonOptions);
        var deserialized = JsonSerializer.Deserialize<SentenceNoteDto>(json, JsonOptions)!;
        var reJson = JsonSerializer.Serialize(deserialized, JsonOptions);

        Assert.Equal(json, reJson);
        Assert.Equal("テストの文です", deserialized.SourceQuestion);
    }

    // The jas_note_id field is stored on the NoteId object, not in the fields dict,
    // so the original GetData() won't have it but FromDto will add it. Exclude from comparison.
    static readonly HashSet<string> FieldsExcludedFromComparison = [MyNoteFields.JasNoteId];

    static bool IsEffectivelyEmpty(string value)
    {
        return string.IsNullOrEmpty(value) || value == "0";
    }

    static void AssertNoteDataFieldsMatch(NoteData original, NoteData roundtripped, string context)
    {
        // Check ID
        Assert.Equal(original.Id, roundtripped.Id);

        // Check tags
        Assert.Equal(original.Tags.OrderBy(t => t).ToList(), roundtripped.Tags.OrderBy(t => t).ToList());

        // Check that all fields from the roundtripped data match the original
        // (roundtripped may have extra empty-equivalent fields that weren't in the original — that's OK)
        foreach (var kvp in roundtripped.Fields)
        {
            if (FieldsExcludedFromComparison.Contains(kvp.Key)) continue;

            var originalValue = original.Fields.TryGetValue(kvp.Key, out var v) ? v : string.Empty;

            // Treat missing/empty original and "0" roundtripped as equivalent
            if (IsEffectivelyEmpty(originalValue) && IsEffectivelyEmpty(kvp.Value)) continue;

            Assert.True(originalValue == kvp.Value,
                $"{context}: Field '{kvp.Key}' mismatch.\n  Original:     [{originalValue}]\n  Roundtripped: [{kvp.Value}]");
        }

        // Check that all original non-empty fields are present in roundtripped
        foreach (var kvp in original.Fields.Where(f => !string.IsNullOrEmpty(f.Value) && !FieldsExcludedFromComparison.Contains(f.Key)))
        {
            Assert.True(roundtripped.Fields.ContainsKey(kvp.Key),
                $"{context}: Original field '{kvp.Key}' with value [{kvp.Value}] missing from roundtripped data");
        }
    }
}
