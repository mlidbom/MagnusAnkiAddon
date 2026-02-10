using System.Collections.Generic;
using System.IO;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Storage;

public class FileSystemNoteRepository : INoteRepository
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

   public void Save(KanjiNote note)
   {
      var path = NoteFilePath(KanjiDir, note.GetId());
      Directory.CreateDirectory(Path.GetDirectoryName(path)!);
      File.WriteAllText(path, _serializer.Serialize(note));
   }

   public void Save(VocabNote note)
   {
      var path = NoteFilePath(VocabDir, note.GetId());
      Directory.CreateDirectory(Path.GetDirectoryName(path)!);
      File.WriteAllText(path, _serializer.Serialize(note));
   }

   public void Save(SentenceNote note)
   {
      var path = NoteFilePath(SentencesDir, note.GetId());
      Directory.CreateDirectory(Path.GetDirectoryName(path)!);
      File.WriteAllText(path, _serializer.Serialize(note));
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
      using var scope = _taskRunner.Current("Loading notes from repository");

      var kanjiFiles = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning kanji files", () => GetJsonFiles(KanjiDir));
      var vocabFiles = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning vocab files", () => GetJsonFiles(VocabDir));
      var sentenceFiles = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning sentence files", () => GetJsonFiles(SentencesDir));

      var threads = ThreadCount.FractionOfLogicalCores(0.4);
      var kanji = scope.ProcessWithProgressAsync(kanjiFiles.Result, path => _serializer.DeserializeKanji(File.ReadAllText(path)), "Loading kanji notes", threads);
      var vocab = scope.ProcessWithProgressAsync(vocabFiles.Result, path => _serializer.DeserializeVocab(File.ReadAllText(path)), "Loading vocab notes", threads);
      var sentences = scope.ProcessWithProgressAsync(sentenceFiles.Result, path => _serializer.DeserializeSentence(File.ReadAllText(path)), "Loading sentence notes", threads);

      return new AllNotesData(kanji.Result, vocab.Result, sentences.Result);
   }

   public void SaveAllSingleFile(AllNotesData data)
   {
      Directory.CreateDirectory(_rootDir);
      File.WriteAllText(AllNotesPath, _serializer.Serialize(data));
   }

   public AllNotesData LoadAllSingleFile() => _serializer.DeserializeAll(File.ReadAllText(AllNotesPath));

   static List<string> GetJsonFiles(string dir) =>
      !Directory.Exists(dir) ? [] : Directory.GetFiles(dir, "*.json", SearchOption.AllDirectories).ToList();

   static string Bucket(NoteId id) => id.Value.ToString("N")[..2];

   static string NoteFilePath(string typeDir, NoteId id) =>
      Path.Combine(typeDir, Bucket(id), $"{id.Value}.json");
}
