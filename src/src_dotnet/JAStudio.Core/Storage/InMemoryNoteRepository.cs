using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.Storage;

public class InMemoryNoteRepository : INoteRepository
{
    readonly Dictionary<NoteId, KanjiNote> _kanji = new();
    readonly Dictionary<NoteId, VocabNote> _vocab = new();
    readonly Dictionary<NoteId, SentenceNote> _sentences = new();

    public void Save(KanjiNote note) => _kanji[note.GetId()] = note;
    public void Save(VocabNote note) => _vocab[note.GetId()] = note;
    public void Save(SentenceNote note) => _sentences[note.GetId()] = note;

    public void Delete(KanjiNote note) => _kanji.Remove(note.GetId());
    public void Delete(VocabNote note) => _vocab.Remove(note.GetId());
    public void Delete(SentenceNote note) => _sentences.Remove(note.GetId());

    public AllNotesData LoadAll() =>
        new([.. _kanji.Values], [.. _vocab.Values], [.. _sentences.Values]);
}
