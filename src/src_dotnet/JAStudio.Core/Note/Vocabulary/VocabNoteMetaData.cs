using System;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMetaData
{
    private readonly Func<VocabNote> _vocab;

    public VocabNoteMetaData(Func<VocabNote> vocab)
    {
        _vocab = vocab;
    }

    private VocabNote Vocab => _vocab();

    public IntegerField SentenceCount => new IntegerField(Vocab, "sentence_count"); // NoteFields.Vocab.sentence_count

    public string MetaTagsHtml(bool displayExtendedSentenceStatistics = true, bool noSentenceStatistics = false)
    {
        // TODO: Implement when vocabnote_meta_tag is ported
        return string.Empty;
    }
}
