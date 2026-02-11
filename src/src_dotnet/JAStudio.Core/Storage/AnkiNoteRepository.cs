using System;
using System.Threading.Tasks;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;
using JAStudio.Core.Anki;
using JAStudio.Core.Note;

namespace JAStudio.Core.Storage;

/// <summary>
/// Loads notes directly from Anki's SQLite database instead of from the filesystem.
/// Save operations are no-ops since Anki is the source of truth in this mode.
/// </summary>
public class AnkiNoteRepository : INoteRepository
{
   readonly NoteServices _noteServices;

   public AnkiNoteRepository(NoteServices noteServices) => _noteServices = noteServices;

   public AllNotesData LoadAll()
   {
      var dbPath = AnkiFacade.Col.DbFilePath()
                ?? throw new InvalidOperationException("Anki collection database is not initialized yet");

      using var scope = _noteServices.TaskRunner.Current("Loading notes from Anki database");

      var vocabBulk = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Loading vocab from Anki", () => NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Vocab, g => new VocabId(g)));
      var kanjiBulk = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Loading kanji from Anki", () => NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Kanji, g => new KanjiId(g)));
      var sentenceBulk = scope.RunOnBackgroundThreadWithSpinningProgressDialogAsync("Loading sentences from Anki", () => NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Sentence, g => new SentenceId(g)));

      // ReSharper disable AccessToDisposedClosure
      var vocab = TaskCE.Run(() => scope.ProcessWithProgress(vocabBulk.Result.Notes, nd => new VocabNote(_noteServices, nd), "Creating vocab notes from anki"));
      var kanji = TaskCE.Run(() => scope.ProcessWithProgress(kanjiBulk.Result.Notes, nd => new KanjiNote(_noteServices, nd), "Creating kanji notes from anki"));
      var sentences = TaskCE.Run(() => scope.ProcessWithProgress(sentenceBulk.Result.Notes, nd => new SentenceNote(_noteServices, nd), "Creating sentence notes from anki"));
      // ReSharper restore AccessToDisposedClosure

      return new AllNotesData(kanji.Result, vocab.Result, sentences.Result);
   }

   public void Save(KanjiNote note)
   {
      throw new NotImplementedException("this should never be called");
   }

   public void Save(VocabNote note)
   {
      throw new NotImplementedException("this should never be called");
   }

   public void Save(SentenceNote note)
   {
      throw new NotImplementedException("this should never be called");
   }
}
