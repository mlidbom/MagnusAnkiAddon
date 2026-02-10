using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Compze.Utilities.Logging;
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

   // Per-type snapshot files
   string KanjiSnapshotPath => Path.Combine(_rootDir, "snapshot_kanji.json");
   string VocabSnapshotPath => Path.Combine(_rootDir, "snapshot_vocab.json");
   string SentencesSnapshotPath => Path.Combine(_rootDir, "snapshot_sentences.json");

   bool HasSnapshot => File.Exists(KanjiSnapshotPath) && File.Exists(VocabSnapshotPath) && File.Exists(SentencesSnapshotPath);

   // Legacy single-file path (kept for SaveAllSingleFile/LoadAllSingleFile test helpers)
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

   public void Delete(KanjiNote note) => DeleteNoteFile(KanjiDir, note.GetId());
   public void Delete(VocabNote note) => DeleteNoteFile(VocabDir, note.GetId());
   public void Delete(SentenceNote note) => DeleteNoteFile(SentencesDir, note.GetId());

   static void DeleteNoteFile(string typeDir, NoteId id)
   {
      var path = NoteFilePath(typeDir, id);
      if(File.Exists(path))
         File.Delete(path);
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
      if(HasSnapshot)
         return LoadWithSnapshot();

      var data = LoadAllFromIndividualFiles();
      if(!data.IsEmpty)
         SaveSnapshot(data);

      return data;
   }

   AllNotesData LoadAllFromIndividualFiles()
   {
      using var scope = _taskRunner.Current("Loading notes from file system");

      var kanjiFiles = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning kanji files", () => GetJsonFiles(KanjiDir));
      var vocabFiles = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning vocab files", () => GetJsonFiles(VocabDir));
      var sentenceFiles = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning sentence files", () => GetJsonFiles(SentencesDir));

      var threads = ThreadCount.FractionOfLogicalCores(0.4);
      var kanji = scope.ProcessWithProgressAsync(kanjiFiles.Result, path => _serializer.DeserializeKanji(File.ReadAllText(path)), "Loading kanji notes", threads);
      var vocab = scope.ProcessWithProgressAsync(vocabFiles.Result, path => _serializer.DeserializeVocab(File.ReadAllText(path)), "Loading vocab notes", threads);
      var sentences = scope.ProcessWithProgressAsync(sentenceFiles.Result, path => _serializer.DeserializeSentence(File.ReadAllText(path)), "Loading sentence notes", threads);

      return new AllNotesData(kanji.Result, vocab.Result, sentences.Result);
   }

   AllNotesData LoadWithSnapshot()
   {
      using var scope = _taskRunner.Current("Loading notes from snapshot");

      var kanjiSnapshotTime = File.GetLastWriteTimeUtc(KanjiSnapshotPath);
      var vocabSnapshotTime = File.GetLastWriteTimeUtc(VocabSnapshotPath);
      var sentencesSnapshotTime = File.GetLastWriteTimeUtc(SentencesSnapshotPath);

      // Stream all 3 snapshot files in parallel — each deserializes + constructs notes in one pass.
      // DeserializeAsyncEnumerable reads one JSON array element at a time, so the full DTO list
      // is never materialized in memory.
      var kanjiTask = Task.Run(async () =>
      {
         using var stream = OpenSequentialRead(KanjiSnapshotPath);
         return await _serializer.DeserializeKanjiStreamAsync(stream);
      });
      var vocabTask = Task.Run(async () =>
      {
         using var stream = OpenSequentialRead(VocabSnapshotPath);
         return await _serializer.DeserializeVocabStreamAsync(stream);
      });
      var sentencesTask = Task.Run(async () =>
      {
         using var stream = OpenSequentialRead(SentencesSnapshotPath);
         return await _serializer.DeserializeSentenceStreamAsync(stream);
      });

      // Scan individual files for incremental patching (runs in parallel with deserialization)
      var kanjiFileInfo = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning kanji files", () => GetJsonFileInfo(KanjiDir));
      var vocabFileInfo = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning vocab files", () => GetJsonFileInfo(VocabDir));
      var sentenceFileInfo = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning sentence files", () => GetJsonFileInfo(SentencesDir));

      Task.WaitAll(kanjiTask, vocabTask, sentencesTask);

      var kanjiById = kanjiTask.Result.ToDictionary(n => n.GetId());
      var vocabById = vocabTask.Result.ToDictionary(n => n.GetId());
      var sentencesById = sentencesTask.Result.ToDictionary(n => n.GetId());

      PatchFromDisk(kanjiById, kanjiFileInfo.Result, kanjiSnapshotTime, _serializer.DeserializeKanji);
      PatchFromDisk(vocabById, vocabFileInfo.Result, vocabSnapshotTime, _serializer.DeserializeVocab);
      PatchFromDisk(sentencesById, sentenceFileInfo.Result, sentencesSnapshotTime, _serializer.DeserializeSentence);

      return new AllNotesData(kanjiById.Values.ToList(), vocabById.Values.ToList(), sentencesById.Values.ToList());
   }

   /// <summary>
   /// Reconciles a snapshot dictionary with the current state on disk:
   /// 1. Removes notes from the dictionary whose individual files no longer exist (deletes).
   /// 2. Replaces/adds notes whose individual files are newer than the snapshot (updates/creates).
   /// </summary>
   static void PatchFromDisk<T>(Dictionary<NoteId, T> lookup, List<NoteFileInfo> filesOnDisk, DateTime snapshotTime, Func<string, T> deserialize) where T : JPNote
   {
      var idsOnDisk = new HashSet<Guid>(filesOnDisk.Count);
      var newerFiles = new List<NoteFileInfo>();

      foreach(var fileInfo in filesOnDisk)
      {
         idsOnDisk.Add(fileInfo.NoteGuid);
         if(fileInfo.LastWriteUtc > snapshotTime)
            newerFiles.Add(fileInfo);
      }

      // Remove notes that were deleted since the snapshot
      var toRemove = lookup.Keys.Where(id => !idsOnDisk.Contains(id.Value)).ToList();
      foreach(var id in toRemove)
         lookup.Remove(id);

      // Patch in notes that were created or updated since the snapshot
      foreach(var fileInfo in newerFiles)
      {
         var note = deserialize(File.ReadAllText(fileInfo.Path));
         lookup[note.GetId()] = note;
      }
   }

   /// <summary>
   /// Atomically writes per-type snapshot files (write temp files, then rename all 3).
   /// 3 parallel writes — each serializes one note at a time via Utf8JsonWriter.
   /// </summary>
   public void SaveSnapshot(AllNotesData data)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime();
      Directory.CreateDirectory(_rootDir);

      var kanjiTmp = KanjiSnapshotPath + ".tmp";
      var vocabTmp = VocabSnapshotPath + ".tmp";
      var sentencesTmp = SentencesSnapshotPath + ".tmp";

      Task.WaitAll(
         Task.Run(() =>
         {
            using var stream = OpenSequentialWrite(kanjiTmp);
            _serializer.SerializeKanjiToStream(data.Kanji, stream);
         }),
         Task.Run(() =>
         {
            using var stream = OpenSequentialWrite(vocabTmp);
            _serializer.SerializeVocabToStream(data.Vocab, stream);
         }),
         Task.Run(() =>
         {
            using var stream = OpenSequentialWrite(sentencesTmp);
            _serializer.SerializeSentenceToStream(data.Sentences, stream);
         })
      );

      // Atomic rename — previous snapshot files remain intact until each rename succeeds
      File.Move(kanjiTmp, KanjiSnapshotPath, overwrite: true);
      File.Move(vocabTmp, VocabSnapshotPath, overwrite: true);
      File.Move(sentencesTmp, SentencesSnapshotPath, overwrite: true);

      // Clean up legacy single-file snapshot if present
      if(File.Exists(AllNotesPath))
         File.Delete(AllNotesPath);
   }

   // --- Kept for backward compatibility with existing tests ---

   public void SaveAllSingleFile(AllNotesData data)
   {
      Directory.CreateDirectory(_rootDir);
      File.WriteAllText(AllNotesPath, _serializer.Serialize(data));
   }

   public AllNotesData LoadAllSingleFile() => _serializer.DeserializeAll(File.ReadAllText(AllNotesPath));

   // --- File helpers ---

   static FileStream OpenSequentialRead(string path) =>
      new(path, FileMode.Open, FileAccess.Read, FileShare.Read, bufferSize: 65536, FileOptions.SequentialScan);

   static FileStream OpenSequentialWrite(string path) =>
      new(path, FileMode.Create, FileAccess.Write, FileShare.None, bufferSize: 65536, FileOptions.SequentialScan);

   static List<string> GetJsonFiles(string dir) =>
      !Directory.Exists(dir) ? [] : Directory.GetFiles(dir, "*.json", SearchOption.AllDirectories).ToList();

   static List<NoteFileInfo> GetJsonFileInfo(string dir)
   {
      if(!Directory.Exists(dir)) return [];

      // Uses DirectoryInfo.EnumerateFiles — timestamps come from the directory
      // enumeration data (FindNextFile on Windows), avoiding a separate stat call per file.
      return new DirectoryInfo(dir)
            .EnumerateFiles("*.json", SearchOption.AllDirectories)
            .Select(fi =>
             {
                var fileName = Path.GetFileNameWithoutExtension(fi.Name);
                return Guid.TryParse(fileName, out var guid)
                          ? new NoteFileInfo(fi.FullName, guid, fi.LastWriteTimeUtc)
                          : null;
             })
            .Where(info => info != null)
            .ToList()!;
   }

   static string Bucket(NoteId id) => id.Value.ToString("N")[..2];

   static string NoteFilePath(string typeDir, NoteId id) =>
      Path.Combine(typeDir, Bucket(id), $"{id.Value}.json");

   record NoteFileInfo(string Path, Guid NoteGuid, DateTime LastWriteUtc);
}
