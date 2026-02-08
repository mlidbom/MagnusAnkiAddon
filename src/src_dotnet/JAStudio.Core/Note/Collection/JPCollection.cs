using System;
using System.Linq;
using System.Threading.Tasks;
using Compze.Utilities.Logging;
using JAStudio.Core.Anki;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core.Note.Collection;

public class JPCollection
{
   public VocabCollection Vocab { get; }
   public KanjiCollection Kanji { get; }
   public SentenceCollection Sentences { get; }

   public JPNote? NoteFromNoteId(long noteId)
   {
      JPNote? note = Vocab.WithIdOrNone(noteId);
      if(note != null) return note;

      note = Kanji.WithIdOrNone(noteId);
      if(note != null) return note;

      return Sentences.WithIdOrNone(noteId);
   }

   public void UpdateCardStudyingStatus(long cardId)
   {
      throw new NotImplementedException();
   }

   public JPCollection(IBackendNoteCreator backendNoteCreator)
   {
      this.Log().Info().LogMethodExecutionTime();

      Vocab = new VocabCollection(backendNoteCreator);
      Kanji = new KanjiCollection(backendNoteCreator);
      Sentences = new SentenceCollection(backendNoteCreator);
   }

   public void SetNoteServices(NoteServices noteServices)
   {
      Vocab.Cache.SetNoteServices(noteServices);
      Kanji.Cache.SetNoteServices(noteServices);
      Sentences.Cache.SetNoteServices(noteServices);

      if(!TestEnvDetector.IsTesting)
         LoadFromAnkiDatabase(noteServices);
   }

   void LoadFromAnkiDatabase(NoteServices noteServices)
   {
      using var _ = this.Log().Warning().LogMethodExecutionTime();
      var dbPath = AnkiFacade.Col.DbFilePath();

      // Each loader opens its own connection, so it's safe to run on any thread.
      var vocabData = NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Vocab);
      var kanjiData = NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Kanji);
      var sentenceData = NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Sentence);
      var studyingStatuses = CardStudyingStatusLoader.FetchAll(dbPath);

      // Push into caches in parallel — each note type has its own cache with no shared
      // mutable state, so concurrent writes are safe. Each runner gets its own progress
      // panel in the shared MultiTaskProgressDialog.
      using var vocabRunner = noteServices.TaskRunner.Create("Loading notes", "Loading vocab...");
      using var kanjiRunner = noteServices.TaskRunner.Create("Loading notes", "Loading kanji...");
      using var sentenceRunner = noteServices.TaskRunner.Create("Loading notes", "Loading sentences...");

      Task.WhenAll(
         Vocab.Cache.InitFromListAsync(vocabData, vocabRunner),
         Kanji.Cache.InitFromListAsync(kanjiData, kanjiRunner),
         Sentences.Cache.InitFromListAsync(sentenceData, sentenceRunner)
      ).GetAwaiter().GetResult();

      Vocab.Cache.SetStudyingStatuses(studyingStatuses.Where(s => s.NoteTypeName == NoteTypes.Vocab).ToList());
      Kanji.Cache.SetStudyingStatuses(studyingStatuses.Where(s => s.NoteTypeName == NoteTypes.Kanji).ToList());
      Sentences.Cache.SetStudyingStatuses(studyingStatuses.Where(s => s.NoteTypeName == NoteTypes.Sentence).ToList());
   }
}
