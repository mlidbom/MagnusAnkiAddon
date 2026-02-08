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

      using var runner = noteServices.TaskRunner.Current("Loading collection");

      var vocabData = Task.Run(() =>
      {
         //this should get its own panel
         var vocabData = runner.RunOnBackgroundThreadWithSpinningProgressDialog("Fetching Vocabs from anki db", () => NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Vocab));
         return Vocab.Cache.InitFromListAsync(vocabData);
      });

      //this should get its own panel
      var kanjiData = runner.RunOnBackgroundThreadAsync("Fetching Kanji from anki db", () => NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Kanji));
      //this should get its own panel
      var sentenceData = runner.RunOnBackgroundThreadAsync("Fetching Sentences from anki db", () => NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Sentence));
      //this should get its own panel
      var studyingStatuses = runner.RunOnBackgroundThreadAsync("Fetching Studying Statuses from anki db", () => CardStudyingStatusLoader.FetchAll(dbPath));

      //What actually happens, I see only "Fetching Studying Statuses from anki db", none of the others

      Task.WaitAll(kanjiData, sentenceData, studyingStatuses);

      Task.WhenAll(
         vocabData,
         Kanji.Cache.InitFromListAsync(kanjiData.Result),
         Sentences.Cache.InitFromListAsync(sentenceData.Result)
      ).GetAwaiter().GetResult();

      Vocab.Cache.SetStudyingStatuses(studyingStatuses.Result.Where(s => s.NoteTypeName == NoteTypes.Vocab).ToList());
      Kanji.Cache.SetStudyingStatuses(studyingStatuses.Result.Where(s => s.NoteTypeName == NoteTypes.Kanji).ToList());
      Sentences.Cache.SetStudyingStatuses(studyingStatuses.Result.Where(s => s.NoteTypeName == NoteTypes.Sentence).ToList());
   }
}
