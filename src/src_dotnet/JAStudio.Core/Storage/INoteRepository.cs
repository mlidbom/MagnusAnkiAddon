using JAStudio.Core.Note;

namespace JAStudio.Core.Storage;

public interface INoteRepository
{
    void Save(KanjiNote note);
    void Save(VocabNote note);
    void Save(SentenceNote note);

    void Delete(KanjiNote note);
    void Delete(VocabNote note);
    void Delete(SentenceNote note);

    AllNotesData LoadAll();
}
