using System;

namespace JAStudio.Core.Note;

public interface IBackendNoteCreator
{
    void CreateKanji(KanjiNote note, Action callback);
    void CreateVocab(VocabNote note, Action callback);
    void CreateSentence(SentenceNote note, Action callback);
}

public class TestingBackendNoteCreator : IBackendNoteCreator
{
    private int _currentId;

    private int GetNextId()
    {
        _currentId++;
        return _currentId;
    }

    public void CreateKanji(KanjiNote note, Action callback)
    {
        note.SetId(GetNextId());
        callback();
    }

    public void CreateVocab(VocabNote note, Action callback)
    {
        note.SetId(GetNextId());
        callback();
    }

    public void CreateSentence(SentenceNote note, Action callback)
    {
        note.SetId(GetNextId());
        callback();
    }
}
