using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Storage;

public class FileSystemNoteRepository : INoteRepository
{
    readonly Lazy<NoteSerializer> _serializer;
    readonly TaskRunner _taskRunner;
    readonly string _rootDir;

    public FileSystemNoteRepository(Lazy<NoteSerializer> serializer, TaskRunner taskRunner, string rootDir)
    {
        _serializer = serializer;
        _taskRunner = taskRunner;
        _rootDir = rootDir;
    }

    NoteSerializer Serializer => _serializer.Value;

    string KanjiDir => Path.Combine(_rootDir, "kanji");
    string VocabDir => Path.Combine(_rootDir, "vocab");
    string SentencesDir => Path.Combine(_rootDir, "sentences");
    string AllNotesPath => Path.Combine(_rootDir, "all_notes.json");

    public void Save(KanjiNote note)
    {
        var path = NoteFilePath(KanjiDir, note.GetId());
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, Serializer.Serialize(note));
    }

    public void Save(VocabNote note)
    {
        var path = NoteFilePath(VocabDir, note.GetId());
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, Serializer.Serialize(note));
    }

    public void Save(SentenceNote note)
    {
        var path = NoteFilePath(SentencesDir, note.GetId());
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, Serializer.Serialize(note));
    }

    public void SaveAll(AllNotesData data)
    {
       var threads = ThreadCount.HalfLogicalCores;
        using var scope = _taskRunner.Current("Writing all notes to file system repository");
        scope.ProcessWithProgress(data.Kanji, Save, "Saving kanji notes", threads);
        scope.ProcessWithProgress(data.Vocab, Save, "Saving vocab notes", threads);
        scope.ProcessWithProgress(data.Sentences, Save, "Saving sentence notes", threads);
    }

    public AllNotesData LoadAll()
    {
        var kanji = LoadAllFromDir(KanjiDir, Serializer.DeserializeKanji);
        var vocab = LoadAllFromDir(VocabDir, Serializer.DeserializeVocab);
        var sentences = LoadAllFromDir(SentencesDir, Serializer.DeserializeSentence);
        return new AllNotesData(kanji, vocab, sentences);
    }

    public void SaveAllSingleFile(AllNotesData data)
    {
        Directory.CreateDirectory(_rootDir);
        File.WriteAllText(AllNotesPath, Serializer.Serialize(data));
    }

    public AllNotesData LoadAllSingleFile()
    {
        return Serializer.DeserializeAll(File.ReadAllText(AllNotesPath));
    }

    static List<T> LoadAllFromDir<T>(string dir, System.Func<string, T> deserialize)
    {
        if (!Directory.Exists(dir)) return [];
        return Directory.GetFiles(dir, "*.json", SearchOption.AllDirectories)
            .Select(File.ReadAllText)
            .Select(deserialize)
            .ToList();
    }

    static string Bucket(NoteId id) => id.Value.ToString("N")[..2];

    static string NoteFilePath(string typeDir, NoteId id) =>
        Path.Combine(typeDir, Bucket(id), $"{id.Value}.json");
}
