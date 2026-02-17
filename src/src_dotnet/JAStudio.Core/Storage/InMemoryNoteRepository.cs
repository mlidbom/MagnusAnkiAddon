using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.Storage;

class InMemoryNoteRepository : INoteRepository
{
   readonly Dictionary<NoteId, KanjiNote> _kanji = new();
   readonly Dictionary<NoteId, VocabNote> _vocab = new();
   readonly Dictionary<NoteId, SentenceNote> _sentences = new();

   public void Save(KanjiNote note) => _kanji[note.GetId()] = note;
   public void Save(VocabNote note) => _vocab[note.GetId()] = note;
   public void Save(SentenceNote note) => _sentences[note.GetId()] = note;

   public AllNotesData LoadAll() =>
      new([.. _kanji.Values], [.. _vocab.Values], [.. _sentences.Values]);
}
