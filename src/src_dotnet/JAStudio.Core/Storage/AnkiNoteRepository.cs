using System.Linq;
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

   public AnkiNoteRepository(NoteServices noteServices)
   {
      _noteServices = noteServices;
   }

   public AllNotesData LoadAll()
   {
      var dbPath = AnkiFacade.Col.DbFilePath()
                   ?? throw new System.InvalidOperationException("Anki collection database is not initialized yet");

      var vocabBulk = NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Vocab, g => new VocabId(g));
      var kanjiBulk = NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Kanji, g => new KanjiId(g));
      var sentenceBulk = NoteBulkLoader.LoadAllNotesOfType(dbPath, NoteTypes.Sentence, g => new SentenceId(g));

      var vocab = vocabBulk.Notes.Select(nd => new VocabNote(_noteServices, nd)).ToList();
      var kanji = kanjiBulk.Notes.Select(nd => new KanjiNote(_noteServices, nd)).ToList();
      var sentences = sentenceBulk.Notes.Select(nd => new SentenceNote(_noteServices, nd)).ToList();

      return new AllNotesData(kanji, vocab, sentences);
   }

   public void Save(KanjiNote note) { /* No-op: Anki is the source of truth in this mode */ }
   public void Save(VocabNote note) { /* No-op: Anki is the source of truth in this mode */ }
   public void Save(SentenceNote note) { /* No-op: Anki is the source of truth in this mode */ }
}
