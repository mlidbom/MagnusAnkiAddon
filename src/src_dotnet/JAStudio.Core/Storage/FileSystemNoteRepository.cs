using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using JAStudio.Core.Note;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Storage;

public class FileSystemNoteRepository : INoteRepository
{
   readonly NoteSerializer _serializer;
   readonly TaskRunner _taskRunner;
   readonly string _rootDir;

   public NoteSerializer Serializer => _serializer;

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

   /// <summary>
   /// Returns partitioned file paths without deserializing. Used by JPCollection
   /// to deserialize and push to cache in a single pass per type.
   /// </summary>
   public NoteFilesByType ScanFiles()
   {
      using var scope = _taskRunner.Current("Scanning note files");
      return scope.RunOnBackgroundThreadWithSpinningProgressDialog("Scanning note files", ScanAllNoteFiles);
   }

   public AllNotesData LoadAll()
   {
      var filesByType = ScanFiles();

      using var scope = _taskRunner.Current("Loading notes from file system");
      var kanji = scope.ProcessWithProgressAsync(filesByType.Kanji, path => _serializer.DeserializeKanji(File.ReadAllText(path)), "Loading kanji notes", ThreadCount.One);
      var vocab = scope.ProcessWithProgressAsync(filesByType.Vocab, path => _serializer.DeserializeVocab(File.ReadAllText(path)), "Loading vocab notes", ThreadCount.FractionOfLogicalCores(0.3));
      var sentences = scope.ProcessWithProgressAsync(filesByType.Sentences, path => _serializer.DeserializeSentence(File.ReadAllText(path)), "Loading sentence notes", ThreadCount.FractionOfLogicalCores(0.5));

      return new AllNotesData(kanji.Result, vocab.Result, sentences.Result);
   }

   public void SaveAllSingleFile(AllNotesData data)
   {
      Directory.CreateDirectory(_rootDir);
      File.WriteAllText(AllNotesPath, _serializer.Serialize(data));
   }

   public AllNotesData LoadAllSingleFile() => _serializer.DeserializeAll(File.ReadAllText(AllNotesPath));

   /// <summary>
   /// Single directory walk from root — enumerates all *.json note files once,
   /// partitions them into kanji/vocab/sentences based on which subdirectory they live under.
   /// </summary>
   NoteFilesByType ScanAllNoteFiles()
   {
      var kanji = new List<string>();
      var vocab = new List<string>();
      var sentences = new List<string>();

      if(!Directory.Exists(_rootDir)) return new NoteFilesByType(kanji, vocab, sentences);

      var kanjiPrefix = KanjiDir + Path.DirectorySeparatorChar;
      var vocabPrefix = VocabDir + Path.DirectorySeparatorChar;
      var sentencesPrefix = SentencesDir + Path.DirectorySeparatorChar;

      foreach(var fi in new DirectoryInfo(_rootDir).EnumerateFiles("*.json", SearchOption.AllDirectories))
      {
         var fullName = fi.FullName;
         if(fullName.StartsWith(kanjiPrefix, StringComparison.OrdinalIgnoreCase))
            kanji.Add(fullName);
         else if(fullName.StartsWith(vocabPrefix, StringComparison.OrdinalIgnoreCase))
            vocab.Add(fullName);
         else if(fullName.StartsWith(sentencesPrefix, StringComparison.OrdinalIgnoreCase))
            sentences.Add(fullName);
      }

      return new NoteFilesByType(kanji, vocab, sentences);
   }

   static string Bucket(NoteId id) => id.Value.ToString("N")[..2];

   static string NoteFilePath(string typeDir, NoteId id) =>
      Path.Combine(typeDir, Bucket(id), $"{id.Value}.json");

   public record NoteFilesByType(List<string> Kanji, List<string> Vocab, List<string> Sentences);
}
