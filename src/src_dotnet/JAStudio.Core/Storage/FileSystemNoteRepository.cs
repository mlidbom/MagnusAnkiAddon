using System.Collections.Generic;
using System.IO;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Storage;

public class FileSystemNoteRepository
{
    readonly NoteSerializer _serializer;
    readonly TaskRunner _taskRunner;
    readonly string _rootDir;

    public FileSystemNoteRepository(NoteSerializer serializer, TaskRunner taskRunner, string rootDir)
    {
        _serializer = serializer;
        _taskRunner = taskRunner;
        _rootDir = rootDir;
    }

    string KanjiDir => Path.Combine(_rootDir, "kanji");
    string VocabDir => Path.Combine(_rootDir, "vocab");
    string SentencesDir => Path.Combine(_rootDir, "sentences");
    string AllNotesPath => Path.Combine(_rootDir, "all_notes.json");

    public void SaveKanji(KanjiNote note)
    {
        var path = NoteFilePath(KanjiDir, note.GetId());
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, _serializer.Serialize(note));
    }

    public KanjiNote LoadKanji(NoteId id)
    {
        return _serializer.DeserializeKanji(File.ReadAllText(NoteFilePath(KanjiDir, id)));
    }

    public void SaveVocab(VocabNote note)
    {
        var path = NoteFilePath(VocabDir, note.GetId());
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, _serializer.Serialize(note));
    }

    public VocabNote LoadVocab(NoteId id)
    {
        return _serializer.DeserializeVocab(File.ReadAllText(NoteFilePath(VocabDir, id)));
    }

    public void SaveSentence(SentenceNote note)
    {
        var path = NoteFilePath(SentencesDir, note.GetId());
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, _serializer.Serialize(note));
    }

    public SentenceNote LoadSentence(NoteId id)
    {
        return _serializer.DeserializeSentence(File.ReadAllText(NoteFilePath(SentencesDir, id)));
    }

    public void SaveAll(AllNotesData data)
    {
       var threads = ThreadCount.HalfLogicalCores;
        using var scope = _taskRunner.Current("Writing all notes to file system repository");
        scope.ProcessWithProgress(data.Kanji, SaveKanji, "Saving kanji notes", threads);
        scope.ProcessWithProgress(data.Vocab, SaveVocab, "Saving vocab notes", threads);
        scope.ProcessWithProgress(data.Sentences, SaveSentence, "Saving sentence notes", threads);
    }

    public AllNotesData LoadAll()
    {
        var kanji = LoadAllFromDir(KanjiDir, _serializer.DeserializeKanji);
        var vocab = LoadAllFromDir(VocabDir, _serializer.DeserializeVocab);
        var sentences = LoadAllFromDir(SentencesDir, _serializer.DeserializeSentence);
        return new AllNotesData(kanji, vocab, sentences);
    }

    public void SaveAllSingleFile(AllNotesData data)
    {
        Directory.CreateDirectory(_rootDir);
        File.WriteAllText(AllNotesPath, _serializer.Serialize(data));
    }

    public AllNotesData LoadAllSingleFile()
    {
        return _serializer.DeserializeAll(File.ReadAllText(AllNotesPath));
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
