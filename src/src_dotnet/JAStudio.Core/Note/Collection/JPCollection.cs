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
      JPNote? note = Vocab.WithAnkiIdOrNone(ankiNoteId);
      if(note != null) return note;

      note = Kanji.WithAnkiIdOrNone(ankiNoteId);
      if(note != null) return note;

      return Sentences.WithAnkiIdOrNone(ankiNoteId);
   }

   /// <summary>
   /// Returns the Anki long note ID for the given domain NoteId.
   /// Used at the Python boundary where Anki's numeric ID is needed.
   /// Returns 0 if no mapping found.
   /// </summary>
   public long GetAnkiNoteId(NoteId noteId)
   {
      var ankiId = Vocab.Cache.GetAnkiNoteId(noteId);
      if(ankiId != 0) return ankiId;

      ankiId = Kanji.Cache.GetAnkiNoteId(noteId);
      if(ankiId != 0) return ankiId;

      return Sentences.Cache.GetAnkiNoteId(noteId);
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

      using var runner = noteServices.TaskRunner.Current("Loading collection");

      var studyingStatuses = runner.RunOnBackgroundThreadAsync("Fetching Studying Statuses from anki db", () => CardStudyingStatusLoader.FetchAll(dbPath));
      var vocabData = Vocab.Cache.LoadAsync();
      var kanjiData = Kanji.Cache.LoadAsync();
      var sentenceData = Sentences.Cache.LoadAsync();

      Task.WaitAll(kanjiData, sentenceData, vocabData, studyingStatuses);

      // Group studying statuses by Anki note ID for efficient lookup
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

      Vocab.Cache.SetStudyingStatuses(vocabStatuses);
      Kanji.Cache.SetStudyingStatuses(kanjiStatuses);
      Sentences.Cache.SetStudyingStatuses(sentenceStatuses);
   }
}
