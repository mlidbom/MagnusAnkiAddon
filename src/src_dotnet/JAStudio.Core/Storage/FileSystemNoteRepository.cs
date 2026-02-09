using System.Collections.Generic;
using System.IO;
using System.Linq;
using JAStudio.Core.Note;

namespace JAStudio.Core.Storage;

public class FileSystemNoteRepository
{
    readonly NoteSerializer _serializer;
    readonly string _rootDir;

    public FileSystemNoteRepository(NoteSerializer serializer, string rootDir)
    {
        _serializer = serializer;
        _rootDir = rootDir;
    }

    string KanjiDir => Path.Combine(_rootDir, "kanji");
    string VocabDir => Path.Combine(_rootDir, "vocab");
    string SentencesDir => Path.Combine(_rootDir, "sentences");
    string AllNotesPath => Path.Combine(_rootDir, "all_notes.json");

    public void SaveKanji(KanjiNote note)
    {
        Directory.CreateDirectory(KanjiDir);
        File.WriteAllText(KanjiFilePath(note.GetId()), _serializer.Serialize(note));
    }

    public KanjiNote LoadKanji(NoteId id)
    {
        return _serializer.DeserializeKanji(File.ReadAllText(KanjiFilePath(id)));
    }

    public void SaveVocab(VocabNote note)
    {
        Directory.CreateDirectory(VocabDir);
        File.WriteAllText(VocabFilePath(note.GetId()), _serializer.Serialize(note));
    }

    public VocabNote LoadVocab(NoteId id)
    {
        return _serializer.DeserializeVocab(File.ReadAllText(VocabFilePath(id)));
    }

    public void SaveSentence(SentenceNote note)
    {
        Directory.CreateDirectory(SentencesDir);
        File.WriteAllText(SentenceFilePath(note.GetId()), _serializer.Serialize(note));
    }

    public SentenceNote LoadSentence(NoteId id)
    {
        return _serializer.DeserializeSentence(File.ReadAllText(SentenceFilePath(id)));
    }

    public void SaveAll(AllNotesData data)
    {
        foreach (var note in data.Kanji) SaveKanji(note);
        foreach (var note in data.Vocab) SaveVocab(note);
        foreach (var note in data.Sentences) SaveSentence(note);
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
        return Directory.GetFiles(dir, "*.json")
            .Select(File.ReadAllText)
            .Select(deserialize)
            .ToList();
    }

    string KanjiFilePath(NoteId id) => Path.Combine(KanjiDir, $"{id.Value}.json");
    string VocabFilePath(NoteId id) => Path.Combine(VocabDir, $"{id.Value}.json");
    string SentenceFilePath(NoteId id) => Path.Combine(SentencesDir, $"{id.Value}.json");
}
