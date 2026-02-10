using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
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
      if(File.Exists(AllNotesPath))
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
      using var scope = _taskRunner.Current("Loading notes from snapshot + incremental files");
      var snapshotTime = File.GetLastWriteTimeUtc(AllNotesPath);

      var snapshotData = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync(
         "Loading snapshot file",
         () => _serializer.DeserializeAll(File.ReadAllText(AllNotesPath)));

      // Scan all individual files in parallel — we need both the set of current IDs (for delete detection)
      // and the list of files newer than the snapshot (for patching).
      var kanjiFileInfo = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning kanji files", () => GetJsonFileInfo(KanjiDir));
      var vocabFileInfo = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning vocab files", () => GetJsonFileInfo(VocabDir));
      var sentenceFileInfo = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Scanning sentence files", () => GetJsonFileInfo(SentencesDir));

      var snapshot = snapshotData.Result;

      var kanjiById = snapshot.Kanji.ToDictionary(n => n.GetId());
      var vocabById = snapshot.Vocab.ToDictionary(n => n.GetId());
      var sentencesById = snapshot.Sentences.ToDictionary(n => n.GetId());

      PatchFromDisk(kanjiById, kanjiFileInfo.Result, snapshotTime, _serializer.DeserializeKanji);
      PatchFromDisk(vocabById, vocabFileInfo.Result, snapshotTime, _serializer.DeserializeVocab);
      PatchFromDisk(sentencesById, sentenceFileInfo.Result, snapshotTime, _serializer.DeserializeSentence);

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
   /// Atomically writes the snapshot file (write to temp, then rename).
   /// Safe against crashes mid-write — the old snapshot remains intact until the rename succeeds.
   /// </summary>
   public void SaveSnapshot(AllNotesData data)
   {
      using var _ = this.Log().Info().LogMethodExecutionTime();
      Directory.CreateDirectory(_rootDir);
      var tempPath = AllNotesPath + ".tmp";
      File.WriteAllText(tempPath, _serializer.Serialize(data));
      File.Move(tempPath, AllNotesPath, overwrite: true);
   }

   // --- Kept for backward compatibility with existing tests ---

   public void SaveAllSingleFile(AllNotesData data)
   {
      Directory.CreateDirectory(_rootDir);
      File.WriteAllText(AllNotesPath, _serializer.Serialize(data));
   }

   public AllNotesData LoadAllSingleFile() => _serializer.DeserializeAll(File.ReadAllText(AllNotesPath));

   // --- File scanning helpers ---

   static List<string> GetJsonFiles(string dir) =>
      !Directory.Exists(dir) ? [] : Directory.GetFiles(dir, "*.json", SearchOption.AllDirectories).ToList();

   static List<NoteFileInfo> GetJsonFileInfo(string dir)
   {
      if(!Directory.Exists(dir)) return [];

      return Directory.GetFiles(dir, "*.json", SearchOption.AllDirectories)
                      .Select(path =>
                       {
                          var fileName = Path.GetFileNameWithoutExtension(path);
                          return Guid.TryParse(fileName, out var guid)
                                    ? new NoteFileInfo(path, guid, File.GetLastWriteTimeUtc(path))
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
