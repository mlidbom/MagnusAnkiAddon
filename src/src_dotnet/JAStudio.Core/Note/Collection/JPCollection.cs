using System;
using System.Linq;
using System.Threading.Tasks;
using Compze.Utilities.Logging;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;
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
   /// Look up a note by its external long ID. Used at the Python boundary where
   /// only external IDs are available (e.g. from card.nid, note.id).
   /// </summary>
   public JPNote? NoteFromExternalId(long externalNoteId)
   {
      var noteId = NoteServices.ExternalNoteIdMap.FromExternalId(externalNoteId);
      return noteId != null ? NoteFromNoteId(noteId) : null;
   }

   /// <summary>
   /// Returns the external long note ID for the given domain NoteId.
   /// Used at the Python boundary where the external numeric ID is needed.
   /// Returns 0 if no mapping found.
   /// </summary>
   public long GetExternalNoteId(NoteId noteId) => NoteServices.ExternalNoteIdMap.ToExternalId(noteId) ?? 0;

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
      INoteRepository noteRepository,
      IBackendDataLoader? backendDataLoader = null)
   {
      this.Log().Info().LogMethodExecutionTime();

      NoteServices = noteServices;
      _repository = noteRepository;
      _backendDataLoader = backendDataLoader;
      DictLookup = new DictLookup(this, config);
      VocabNoteGeneratedData = new VocabNoteGeneratedData(DictLookup);
      VocabNoteFactory = new VocabNoteFactory(DictLookup, this, noteServices);

      Vocab = new VocabCollection(backendNoteCreator, NoteServices);
      Kanji = new KanjiCollection(backendNoteCreator, NoteServices);
      Sentences = new SentenceCollection(backendNoteCreator, NoteServices);

      Kanji.Cache.OnNoteUpdated(note => _repository.Save(note));
      Vocab.Cache.OnNoteUpdated(note => _repository.Save(note));
      Sentences.Cache.OnNoteUpdated(note => _repository.Save(note));
   }

   readonly INoteRepository _repository;
   readonly IBackendDataLoader? _backendDataLoader;

   /// <summary>Clear all in-memory caches. Called when the backend DB is about to become unreliable (e.g. sync starting, profile closing).</summary>
   public void ClearCaches()
   {
      using var _ = this.Log().Warning().LogMethodExecutionTime();
      NoteServices.ExternalNoteIdMap.Clear();
      Vocab.Cache.Clear();
      Kanji.Cache.Clear();
      Sentences.Cache.Clear();
   }

   /// <summary>Clear and reload all caches. Called after sync or collection reload.</summary>
   public void ReloadFromBackend()
   {
      using var runner = NoteServices.TaskRunner.Current("Populating caches from file system");
      // ReSharper disable once ExplicitCallerInfoArgument
      using var _ = this.Log().Info().LogMethodExecutionTime("====== Reloading JAStudio data ======");

      ClearCaches();
      var repoLoad = TaskCE.Run(LoadFromRepository);

      Task<BackendData?> backendDataTask = _backendDataLoader != null
                                              ? Task.Run(() => (BackendData?)_backendDataLoader.Load(NoteServices.TaskRunner))
                                              : Task.FromResult<BackendData?>(null);

      Task.WaitAll(repoLoad, backendDataTask);

      var backendData = backendDataTask.Result;
      if(backendData != null)
      {
         foreach(var (externalId, noteId) in backendData.IdMappings)
            NoteServices.ExternalNoteIdMap.Register(externalId, noteId);

         var vocabStatuses = backendData.StudyingStatuses
                                        .Where(s => s.NoteTypeName == NoteTypes.Vocab)
                                        .GroupBy(s => s.ExternalNoteId)
                                        .ToDictionary(g => g.Key, g => g.ToList());
         var kanjiStatuses = backendData.StudyingStatuses
                                        .Where(s => s.NoteTypeName == NoteTypes.Kanji)
                                        .GroupBy(s => s.ExternalNoteId)
                                        .ToDictionary(g => g.Key, g => g.ToList());
         var sentenceStatuses = backendData.StudyingStatuses
                                           .Where(s => s.NoteTypeName == NoteTypes.Sentence)
                                           .GroupBy(s => s.ExternalNoteId)
                                           .ToDictionary(g => g.Key, g => g.ToList());

         runner.RunIndeterminate("Setting studying statuses",
                                 () =>
                                 {
                                    Vocab.Cache.SetStudyingStatuses(vocabStatuses);
                                    Kanji.Cache.SetStudyingStatuses(kanjiStatuses);
                                    Sentences.Cache.SetStudyingStatuses(sentenceStatuses);
                                 });
      }
   }

   void LoadFromRepository()
   {
      using var _ = this.Log().Warning().LogMethodExecutionTime();

      var allNotes = _repository.LoadAll();

      using var runner = NoteServices.TaskRunner.Current("Populating caches from file system");

      Task.WaitAll(
         runner.RunIndeterminateAsync("Pushing kanji notes into cache", () => Kanji.Cache.AddAllToCache(allNotes.Kanji)),
         runner.RunIndeterminateAsync("Pushing vocab notes into cache", () => Vocab.Cache.AddAllToCache(allNotes.Vocab)),
         runner.RunIndeterminateAsync("Pushing sentence notes into cache", () => Sentences.Cache.AddAllToCache(allNotes.Sentences)));
   }
}
