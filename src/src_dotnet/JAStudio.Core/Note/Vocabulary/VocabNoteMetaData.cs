using JAStudio.Core.Note.ReactiveProperties;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMetaData
{
    private readonly VocabNote _vocab;

    public IntProperty SentenceCount { get; }

    public VocabNoteMetaData(VocabNote vocab, StringProperty sentenceCountField)
    {
        _vocab = vocab;
        SentenceCount = new IntProperty(sentenceCountField);
    }

    private VocabNote Vocab => _vocab;

    public string MetaTagsHtml(bool displayExtendedSentenceStatistics = true, bool noSentenceStatistics = false)
    {
        return VocabNoteMetaTagFormatter.GetMetaTagsHtml(Vocab, displayExtendedSentenceStatistics, noSentenceStatistics);
    }
}
