using System;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteUserFields
{
    private readonly VocabNote _vocab;
    private readonly Func<string, string> _getField;
    private readonly Action<string, string> _setField;
    public readonly CachingMutableStringField Answer;

    public VocabNoteUserFields(VocabNote vocab, Func<string, string> getField, Action<string, string> setField)
    {
        _vocab = vocab;
        _getField = getField;
        _setField = setField;
        Answer = new CachingMutableStringField(NoteFieldsConstants.Vocab.UserAnswer, getField, setField);
    }

    public MutableStringField Mnemonic => new(NoteFieldsConstants.Vocab.UserMnemonic, _getField, _setField);
    public MutableStringField Explanation => new(NoteFieldsConstants.Vocab.UserExplanation, _getField, _setField);
    public MutableStringField ExplanationLong => new(NoteFieldsConstants.Vocab.UserExplanationLong, _getField, _setField);

    public override string ToString()
    {
        return $"Answer: {Answer.Value}, Mnemonic: {Mnemonic.Value}, Explanation: {Explanation.Value}, Explanation Long: {ExplanationLong.Value}";
    }
}
