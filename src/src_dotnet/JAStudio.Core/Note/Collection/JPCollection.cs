using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;
using JAStudio.Core.Anki;
using JAStudio.Core.Configuration;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Storage;

namespace JAStudio.Core.Note.Collection;

public class JPCollection
{
   public VocabCollection Vocab { get; }
   public KanjiCollection Kanji { get; }
   public SentenceCollection Sentences { get; }

   public JPNote? NoteFromNoteId(NoteId noteId)
   {
      JPNote? note = Vocab.WithIdOrNone(noteId);
      if(note != null) return note;

      note = Kanji.WithIdOrNone(noteId);
      if(note != null) return note;

      return Sentences.WithIdOrNone(noteId);
   }

   /// <summary>
   /// Look up a note by its Anki long ID. Used at the Python boundary where
   /// only Anki IDs are available (e.g. from card.nid, note.id).
   /// </summary>
   public JPNote? NoteFromAnkiNoteId(long ankiNoteId)
   {
      var noteId = NoteServices.AnkiNoteIdMap.FromAnkiId(ankiNoteId);
      return noteId != null ? NoteFromNoteId(noteId) : null;
   }

   /// <summary>
   /// Returns the Anki long note ID for the given domain NoteId.
   /// Used at the Python boundary where Anki's numeric ID is needed.
   /// Returns 0 if no mapping found.
   /// </summary>
   public long GetAnkiNoteId(NoteId noteId) => NoteServices.AnkiNoteIdMap.ToAnkiId(noteId) ?? 0;

   public NoteServices NoteServices { get; }
   public VocabNoteFactory VocabNoteFactory { get; }
   public DictLookup DictLookup { get; }
   public VocabNoteGeneratedData VocabNoteGeneratedData { get; }

   public void UpdateCardStudyingStatus(long cardId)
   {
      throw new NotImplementedException();
   }

   public JPCollection(
      IBackendNoteCreator backendNoteCreator,
      NoteServices noteServices,
      JapaneseConfig config,
      INoteRepository noteRepository)
   {
      this.Log().Info().LogMethodExecutionTime();

      NoteServices = noteServices;
      _noteRepository = noteRepository;
      _config = config;
      DictLookup = new DictLookup(this, config);
      VocabNoteGeneratedData = new VocabNoteGeneratedData(DictLookup);
      VocabNoteFactory = new VocabNoteFactory(DictLookup, this, noteServices);

      Vocab = new VocabCollection(backendNoteCreator, NoteServices);
      Kanji = new KanjiCollection(backendNoteCreator, NoteServices);
      Sentences = new SentenceCollection(backendNoteCreator, NoteServices);

      Kanji.Cache.OnNoteUpdated(note => noteRepository.Save(note));
      Vocab.Cache.OnNoteUpdated(note => noteRepository.Save(note));
      Sentences.Cache.OnNoteUpdated(note => noteRepository.Save(note));
   }

   readonly INoteRepository _noteRepository;
   readonly JapaneseConfig _config;

   /// <summary>Clear all in-memory caches. Called when the Anki DB is about to become unreliable (e.g. sync starting, profile closing).</summary>
   public void ClearCaches()
   {
      using var _ = this.Log().Warning().LogMethodExecutionTime();
      NoteServices.AnkiNoteIdMap.Clear();
      Vocab.Cache.Clear();
      Kanji.Cache.Clear();
      Sentences.Cache.Clear();
   }

   string NoteRepositoryType => _config.LoadNotesFromFileSystem.Value ? "file system" : "anki";

   /// <summary>Clear and reload all caches from the Anki DB. Called after sync or collection reload.</summary>
   public void ReloadFromAnkiDatabase()
   {
      using var runner = NoteServices.TaskRunner.Current($"Populating caches from {NoteRepositoryType}");
      // ReSharper disable once ExplicitCallerInfoArgument
      using var _ = this.Log().Info().LogMethodExecutionTime("====== Reloading JAStudio data ======");

      ClearCaches();
      var repoLoad = TaskCE.Run(LoadFromRepository);

      var studyingStatuses = LoadAnkiUserDataAsync();
      Task.WaitAll(repoLoad, studyingStatuses);

      var vocabStatuses = studyingStatuses.Result
                                          .Where(s => s.NoteTypeName == NoteTypes.Vocab)
                                          .GroupBy(s => s.AnkiNoteId)
                                          .ToDictionary(g => g.Key, g => g.ToList());
      var kanjiStatuses = studyingStatuses.Result
                                          .Where(s => s.NoteTypeName == NoteTypes.Kanji)
                                          .GroupBy(s => s.AnkiNoteId)
                                          .ToDictionary(g => g.Key, g => g.ToList());
      var sentenceStatuses = studyingStatuses.Result
                                             .Where(s => s.NoteTypeName == NoteTypes.Sentence)
                                             .GroupBy(s => s.AnkiNoteId)
                                             .ToDictionary(g => g.Key, g => g.ToList());

      runner.RunOnBackgroundThreadWithSpinningProgressDialog("Setting studying statuses",
                                                             () =>
                                                             {
                                                                Vocab.Cache.SetStudyingStatuses(vocabStatuses);
                                                                Kanji.Cache.SetStudyingStatuses(kanjiStatuses);
                                                                Sentences.Cache.SetStudyingStatuses(sentenceStatuses);
                                                             });
   }

   INoteRepository ConfiguredRepository => _config.LoadNotesFromFileSystem.Value ? _noteRepository : new AnkiNoteRepository(NoteServices);

   void LoadFromRepository()
   {
      using var _ = this.Log().Warning().LogMethodExecutionTime();

      var allNotes = ConfiguredRepository.LoadAll();

      using var runner = NoteServices.TaskRunner.Current($"Populating caches from {NoteRepositoryType}");

      Task.WaitAll(
         runner.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Pushing kanji notes into cache", () => Kanji.Cache.AddAllToCache(allNotes.Kanji)),
         runner.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Pushing vocab notes into cache", () => Vocab.Cache.AddAllToCache(allNotes.Vocab)),
         runner.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Pushing sentence notes into cache", () => Sentences.Cache.AddAllToCache(allNotes.Sentences)));
   }

   async Task<List<CardStudyingStatus>> LoadAnkiUserDataAsync()
   {
      using var _ = this.Log().Warning().LogMethodExecutionTime();
      var dbPath = AnkiFacade.Col.DbFilePath();
      if(dbPath == null) throw new InvalidOperationException("Anki collection database is not initialized yet");

      using var runner = NoteServices.TaskRunner.Current("Loading user data from Anki");

      var ankiIdMapTask = runner.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Loading Anki ID mappings", () => NoteBulkLoader.LoadAnkiIdMaps(dbPath));
      var studyingStatusesTask = runner.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Fetching studying statuses from Anki", () => CardStudyingStatusLoader.FetchAll(dbPath));

      Task.WaitAll(ankiIdMapTask, studyingStatusesTask);

      foreach(var (ankiId, noteId) in ankiIdMapTask.Result)
      {
         NoteServices.AnkiNoteIdMap.Register(ankiId, noteId);
      }

      return await studyingStatusesTask;
   }
}
