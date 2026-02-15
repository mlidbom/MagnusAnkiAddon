using System;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMetaData
{
    private readonly VocabNote _vocab;
    private readonly Func<string, string> _getField;
    private readonly Action<string, string> _setField;

    public VocabNoteMetaData(VocabNote vocab, Func<string, string> getField, Action<string, string> setField)
    {
        _vocab = vocab;
        _getField = getField;
        _setField = setField;
    }

    private VocabNote Vocab => _vocab;

    public IntegerField SentenceCount => new(new MutableStringField(NoteFieldsConstants.Vocab.SentenceCount, _getField, _setField));

    public string MetaTagsHtml(bool displayExtendedSentenceStatistics = true, bool noSentenceStatistics = false)
    {
        return VocabNoteMetaTagFormatter.GetMetaTagsHtml(Vocab, displayExtendedSentenceStatistics, noSentenceStatistics);
    }
}
