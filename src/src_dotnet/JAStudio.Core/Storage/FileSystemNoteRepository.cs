using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Compze.Utilities.Logging;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Storage.Dto;
using JAStudio.Core.TaskRunners;
using MemoryPack;

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
   string SnapshotPath => Path.Combine(_rootDir, "snapshot.bin");

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
      scope.RunBatch(data.Kanji, Save, "Saving kanji notes", threads);
      scope.RunBatch(data.Vocab, Save, "Saving vocab notes", threads);
      scope.RunBatch(data.Sentences, Save, "Saving sentence notes", threads);
   }

   /// <summary>
   /// Returns partitioned file paths without deserializing. Used by JPCollection
   /// to deserialize and push to cache in a single pass per type.
   /// </summary>
   public NoteFilesByType ScanFiles()
   {
      using var scope = _taskRunner.Current("Scanning note files");
      return scope.RunIndeterminate("Scanning note files", ScanAllNoteFiles);
   }

   public AllNotesData LoadAll()
   {
      if(File.Exists(SnapshotPath))
      {
         try
         {
            return LoadWithSnapshotMerge();
         }
         catch(Exception ex)
         {
            this.Log().Error(ex, "Failed to load notes snapshot falling back to full rebuild");
         }
      }

      return LoadAllFromJsonAndSaveSnapshot();
   }

   AllNotesData LoadWithSnapshotMerge()
   {
      using var scope = _taskRunner.Current("Loading notes with snapshot");

      var snapshotTimestamp = File.GetLastWriteTimeUtc(SnapshotPath);
      var container = scope.RunIndeterminate("Loading binary snapshot", DeserializeSnapshot);

      var filesByType = scope.RunIndeterminate("Scanning note files", ScanAllNoteFiles);

      var changes = scope.RunIndeterminate("Finding changes since snapshot", () => FindChangesSinceSnapshot(container, filesByType, snapshotTimestamp));

      if(changes.HasChanges)
      {
         container = scope.RunIndeterminate("Patching snapshot with changes", () => PatchSnapshotWithChanges(container, changes));
         var snapshotToSave = container;
         BackgroundTaskManager.Run(() => SaveSnapshotContainer(snapshotToSave));
      }

      return _serializer.ContainerToAllNotesData(container);
   }

   SnapshotChanges FindChangesSinceSnapshot(AllNotesContainer container, NoteFilesByType filesByType, DateTime snapshotTimestamp)
   {
      var currentKanjiIds = filesByType.Kanji.Select(f => f.Id).ToHashSet();
      var currentVocabIds = filesByType.Vocab.Select(f => f.Id).ToHashSet();
      var currentSentenceIds = filesByType.Sentences.Select(f => f.Id).ToHashSet();

      var changedKanji = filesByType.Kanji.Where(f => f.LastWriteUtc > snapshotTimestamp).ToList();
      var changedVocab = filesByType.Vocab.Where(f => f.LastWriteUtc > snapshotTimestamp).ToList();
      var changedSentences = filesByType.Sentences.Where(f => f.LastWriteUtc > snapshotTimestamp).ToList();

      var deletedKanjiCount = container.Kanji.Count(d => !currentKanjiIds.Contains(d.Id));
      var deletedVocabCount = container.Vocab.Count(d => !currentVocabIds.Contains(d.Id));
      var deletedSentencesCount = container.Sentences.Count(d => !currentSentenceIds.Contains(d.Id));

      return new SnapshotChanges(
         changedKanji, changedVocab, changedSentences,
         currentKanjiIds, currentVocabIds, currentSentenceIds,
         deletedKanjiCount + deletedVocabCount + deletedSentencesCount);
   }

   AllNotesContainer PatchSnapshotWithChanges(AllNotesContainer container, SnapshotChanges changes)
   {
      var kanjiMap = container.Kanji.ToDictionary(d => d.Id);
      var vocabMap = container.Vocab.ToDictionary(d => d.Id);
      var sentencesMap = container.Sentences.ToDictionary(d => d.Id);

      foreach(var file in changes.ChangedKanji)
         kanjiMap[file.Id] = _serializer.DeserializeKanjiToData(File.ReadAllText(file.Path));
      foreach(var file in changes.ChangedVocab)
         vocabMap[file.Id] = _serializer.DeserializeVocabToData(File.ReadAllText(file.Path));
      foreach(var file in changes.ChangedSentences)
         sentencesMap[file.Id] = _serializer.DeserializeSentenceToData(File.ReadAllText(file.Path));

      foreach(var id in kanjiMap.Keys.Where(id => !changes.CurrentKanjiIds.Contains(id)).ToList())
         kanjiMap.Remove(id);
      foreach(var id in vocabMap.Keys.Where(id => !changes.CurrentVocabIds.Contains(id)).ToList())
         vocabMap.Remove(id);
      foreach(var id in sentencesMap.Keys.Where(id => !changes.CurrentSentenceIds.Contains(id)).ToList())
         sentencesMap.Remove(id);

      return new AllNotesContainer
      {
         Kanji = kanjiMap.Values.ToList(),
         Vocab = vocabMap.Values.ToList(),
         Sentences = sentencesMap.Values.ToList(),
      };
   }

   record SnapshotChanges(
      List<ScannedFile> ChangedKanji,
      List<ScannedFile> ChangedVocab,
      List<ScannedFile> ChangedSentences,
      HashSet<Guid> CurrentKanjiIds,
      HashSet<Guid> CurrentVocabIds,
      HashSet<Guid> CurrentSentenceIds,
      int DeletedCount)
   {
      public bool HasChanges => ChangedKanji.Count + ChangedVocab.Count + ChangedSentences.Count + DeletedCount > 0;
   }

   AllNotesData LoadAllFromJsonAndSaveSnapshot()
   {
      var allNotes = LoadAllFromJson();
      SaveSnapshot(allNotes);
      return allNotes;
   }

   AllNotesData LoadAllFromJson()
   {
      var filesByType = ScanFiles();

      using var scope = _taskRunner.Current("Loading notes from file system");
      var kanji = scope.RunBatchAsync(filesByType.Kanji, f => _serializer.DeserializeKanji(File.ReadAllText(f.Path)), "Loading kanji notes", ThreadCount.One);
      var vocab = scope.RunBatchAsync(filesByType.Vocab, f => _serializer.DeserializeVocab(File.ReadAllText(f.Path)), "Loading vocab notes", ThreadCount.FractionOfLogicalCores(0.3));
      var sentences = scope.RunBatchAsync(filesByType.Sentences, f => _serializer.DeserializeSentence(File.ReadAllText(f.Path)), "Loading sentence notes", ThreadCount.FractionOfLogicalCores(0.5));

      return new AllNotesData(kanji.Result, vocab.Result, sentences.Result);
   }

   public void SaveSnapshot(AllNotesData data)
   {
      var container = _serializer.AllNotesDataToContainer(data);
      SaveSnapshotContainer(container);
   }

   void SaveSnapshotContainer(AllNotesContainer container)
   {
      Directory.CreateDirectory(_rootDir);
      using var stream = File.Create(SnapshotPath);
      MemoryPackSerializer.SerializeAsync(stream, container).GetAwaiter().GetResult();
   }

   AllNotesContainer DeserializeSnapshot()
   {
      using var stream = File.OpenRead(SnapshotPath);
      return MemoryPackSerializer.DeserializeAsync<AllNotesContainer>(stream).GetAwaiter().GetResult()
             ?? throw new InvalidOperationException("Snapshot deserialization returned null");
   }

   public AllNotesData LoadSnapshot() => _serializer.ContainerToAllNotesData(DeserializeSnapshot());

   /// <summary>
   /// Single directory walk from root — enumerates all *.json note files once,
   /// partitions them into kanji/vocab/sentences based on which subdirectory they live under.
   /// </summary>
   NoteFilesByType ScanAllNoteFiles()
   {
      var kanji = new List<ScannedFile>();
      var vocab = new List<ScannedFile>();
      var sentences = new List<ScannedFile>();

      if(!Directory.Exists(_rootDir)) return new NoteFilesByType(kanji, vocab, sentences);

      var kanjiPrefix = KanjiDir + Path.DirectorySeparatorChar;
      var vocabPrefix = VocabDir + Path.DirectorySeparatorChar;
      var sentencesPrefix = SentencesDir + Path.DirectorySeparatorChar;

      foreach(var fi in new DirectoryInfo(_rootDir).EnumerateFiles("*.json", SearchOption.AllDirectories))
      {
         var fullName = fi.FullName;
         var scanned = new ScannedFile(fullName, Guid.Parse(Path.GetFileNameWithoutExtension(fullName)), fi.LastWriteTimeUtc);
         if(fullName.StartsWith(kanjiPrefix, StringComparison.OrdinalIgnoreCase))
            kanji.Add(scanned);
         else if(fullName.StartsWith(vocabPrefix, StringComparison.OrdinalIgnoreCase))
            vocab.Add(scanned);
         else if(fullName.StartsWith(sentencesPrefix, StringComparison.OrdinalIgnoreCase))
            sentences.Add(scanned);
      }

      return new NoteFilesByType(kanji, vocab, sentences);
   }

   static string Bucket(NoteId id) => id.Value.ToString("N")[..2];

   static string NoteFilePath(string typeDir, NoteId id) =>
      Path.Combine(typeDir, Bucket(id), $"{id.Value}.json");

   public record ScannedFile(string Path, Guid Id, DateTime LastWriteUtc);
   public record NoteFilesByType(List<ScannedFile> Kanji, List<ScannedFile> Vocab, List<ScannedFile> Sentences);
}
