using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Storage;
using JAStudio.Core.TaskRunners;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Storage;

public class FileSystemNoteRepositoryTests : CollectionUsingTest, IDisposable
{
    readonly NoteSerializer _serializer;
    readonly string _tempDir;
    readonly FileSystemNoteRepository _repo;

    public FileSystemNoteRepositoryTests() : base(DataNeeded.All)
    {
        _serializer = GetService<NoteSerializer>();
        _tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");
        _repo = new FileSystemNoteRepository(_serializer, GetService<TaskRunner>(), _tempDir);
    }

    public new void Dispose()
    {
        base.Dispose();
        if (Directory.Exists(_tempDir))
            Directory.Delete(_tempDir, recursive: true);
    }

    // --- Individual kanji note roundtrips ---

    [Fact]
    public void AllKanjiNotes_RoundtripThroughFileSystem()
    {
        var allKanji = NoteServices.Collection.Kanji.All();
        Assert.NotEmpty(allKanji);

        foreach (var kanji in allKanji)
            _repo.Save(kanji);

        var loaded = _repo.LoadAll();
        Assert.Equal(allKanji.Count, loaded.Kanji.Count);

        foreach (var kanji in allKanji)
        {
            var roundtripped = loaded.Kanji.Single(k => k.GetId() == kanji.GetId());
            AssertNoteDataFieldsMatch(kanji.GetData(), roundtripped.GetData(), $"Kanji '{kanji.GetQuestion()}'");
        }
    }

    // --- Individual vocab note roundtrips ---

    [Fact]
    public void AllVocabNotes_RoundtripThroughFileSystem()
    {
        var allVocab = NoteServices.Collection.Vocab.All();
        Assert.NotEmpty(allVocab);

        foreach (var vocab in allVocab)
            _repo.Save(vocab);

        var loaded = _repo.LoadAll();
        Assert.Equal(allVocab.Count, loaded.Vocab.Count);

        foreach (var vocab in allVocab)
        {
            var roundtripped = loaded.Vocab.Single(v => v.GetId() == vocab.GetId());
            AssertNoteDataFieldsMatch(vocab.GetData(), roundtripped.GetData(), $"Vocab '{vocab.GetQuestion()}'");
        }
    }

    // --- Individual sentence note roundtrips ---

    [Fact]
    public void AllSentenceNotes_RoundtripThroughFileSystem()
    {
        var allSentences = NoteServices.Collection.Sentences.All();
        Assert.NotEmpty(allSentences);

        foreach (var sentence in allSentences)
            _repo.Save(sentence);

        var loaded = _repo.LoadAll();
        Assert.Equal(allSentences.Count, loaded.Sentences.Count);

        foreach (var sentence in allSentences)
        {
            var roundtripped = loaded.Sentences.Single(s => s.GetId() == sentence.GetId());
            AssertNoteDataFieldsMatch(sentence.GetData(), roundtripped.GetData(), $"Sentence '{Truncate(sentence.GetQuestion(), 20)}'");
        }
    }

    // --- AllNotesData roundtrip through serializer ---

    [Fact]
    public void AllNotesData_RoundtripThroughSerializer()
    {
        var allData = BuildAllNotesData();

        var json = _serializer.Serialize(allData);
        var roundtripped = _serializer.DeserializeAll(json);

        AssertAllNotesDataMatch(allData, roundtripped);
    }

    // --- AllNotesData save/load individual files ---

    [Fact]
    public void SaveAll_And_LoadAll_PreservesAllFields()
    {
        var allData = BuildAllNotesData();

        _repo.SaveAll(allData);
        var loaded = _repo.LoadAll();

        AssertAllNotesDataMatch(allData, loaded);
    }

    [Fact]
    public void SaveAll_And_LoadAll_PreservesNoteCounts()
    {
        var allData = BuildAllNotesData();

        _repo.SaveAll(allData);
        var loaded = _repo.LoadAll();

        Assert.Equal(allData.Kanji.Count, loaded.Kanji.Count);
        Assert.Equal(allData.Vocab.Count, loaded.Vocab.Count);
        Assert.Equal(allData.Sentences.Count, loaded.Sentences.Count);
    }

    // --- AllNotesData save/load single file ---

    [Fact]
    public void SaveAllSingleFile_And_LoadAllSingleFile_PreservesAllFields()
    {
        var allData = BuildAllNotesData();

        _repo.SaveAllSingleFile(allData);
        var loaded = _repo.LoadAllSingleFile();

        AssertAllNotesDataMatch(allData, loaded);
    }

    [Fact]
    public void SaveAllSingleFile_And_LoadAllSingleFile_ProducesIdenticalJson()
    {
        var allData = BuildAllNotesData();

        _repo.SaveAllSingleFile(allData);
        var loaded = _repo.LoadAllSingleFile();

        var originalJson = _serializer.Serialize(allData);
        var loadedJson = _serializer.Serialize(loaded);

        Assert.Equal(originalJson, loadedJson);
    }

    // --- Helpers ---

    AllNotesData BuildAllNotesData() =>
        new(NoteServices.Collection.Kanji.All(),
            NoteServices.Collection.Vocab.All(),
            NoteServices.Collection.Sentences.All());

    void AssertAllNotesDataMatch(AllNotesData original, AllNotesData roundtripped)
    {
        Assert.Equal(original.Kanji.Count, roundtripped.Kanji.Count);
        Assert.Equal(original.Vocab.Count, roundtripped.Vocab.Count);
        Assert.Equal(original.Sentences.Count, roundtripped.Sentences.Count);

        for (var i = 0; i < original.Kanji.Count; i++)
            AssertNoteDataFieldsMatch(original.Kanji[i].GetData(), roundtripped.Kanji[i].GetData(), $"Kanji '{original.Kanji[i].GetQuestion()}'");

        for (var i = 0; i < original.Vocab.Count; i++)
            AssertNoteDataFieldsMatch(original.Vocab[i].GetData(), roundtripped.Vocab[i].GetData(), $"Vocab '{original.Vocab[i].GetQuestion()}'");

        for (var i = 0; i < original.Sentences.Count; i++)
            AssertNoteDataFieldsMatch(original.Sentences[i].GetData(), roundtripped.Sentences[i].GetData(), $"Sentence '{Truncate(original.Sentences[i].GetQuestion(), 20)}'");
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

        foreach (var kvp in roundtripped.Fields)
        {
            var originalValue = original.Fields.TryGetValue(kvp.Key, out var v) ? v : string.Empty;
            if (IsEffectivelyEmpty(originalValue) && IsEffectivelyEmpty(kvp.Value)) continue;

            Assert.True(originalValue == kvp.Value,
                $"{context}: Field '{kvp.Key}' mismatch.\n  Original:     [{originalValue}]\n  Roundtripped: [{kvp.Value}]");
        }

        foreach (var kvp in original.Fields.Where(f => !string.IsNullOrEmpty(f.Value)))
        {
            Assert.True(roundtripped.Fields.ContainsKey(kvp.Key),
                $"{context}: Original field '{kvp.Key}' with value [{kvp.Value}] missing from roundtripped data");
        }
    }
}
