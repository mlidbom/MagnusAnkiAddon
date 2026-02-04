using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMetaData
{
    private readonly VocabNote _vocab;

    public VocabNoteMetaData(VocabNote vocab)
    {
        _vocab = vocab;
    }

    private VocabNote Vocab => _vocab;

    public IntegerField SentenceCount => new IntegerField(Vocab, NoteFieldsConstants.Vocab.SentenceCount);

    public string MetaTagsHtml(bool displayExtendedSentenceStatistics = true, bool noSentenceStatistics = false)
    {
        return VocabNoteMetaTagFormatter.GetMetaTagsHtml(Vocab, displayExtendedSentenceStatistics, noSentenceStatistics);
    }
}
