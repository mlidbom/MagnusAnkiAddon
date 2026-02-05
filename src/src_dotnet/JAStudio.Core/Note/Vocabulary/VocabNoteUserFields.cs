using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteUserFields
{
    private readonly VocabNote _vocab;
    public readonly CachingMutableStringField Answer;

    public VocabNoteUserFields(VocabNote vocab)
    {
        _vocab = vocab;
        Answer = new CachingMutableStringField(vocab, NoteFieldsConstants.Vocab.UserAnswer);
    }

    public MutableStringField Mnemonic => new(_vocab, NoteFieldsConstants.Vocab.UserMnemonic);
    public MutableStringField Explanation => new(_vocab, NoteFieldsConstants.Vocab.UserExplanation);
    public MutableStringField ExplanationLong => new(_vocab, NoteFieldsConstants.Vocab.UserExplanationLong);

    public override string ToString()
    {
        return $"Answer: {Answer.Value}, Mnemonic: {Mnemonic.Value}, Explanation: {Explanation.Value}, Explanation Long: {ExplanationLong.Value}";
    }
}
