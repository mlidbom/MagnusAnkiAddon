using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteUserFields
{
    readonly NoteGuard _guard;
    string _answer;
    string _mnemonic;
    string _explanation;
    string _explanationLong;

    public WritableStringValue Answer { get; }
    public WritableStringValue Mnemonic { get; }
    public WritableStringValue Explanation { get; }
    public WritableStringValue ExplanationLong { get; }

    public VocabNoteUserFields(VocabData? data, NoteGuard guard)
    {
        _guard = guard;
        _answer = data?.UserAnswer ?? string.Empty;
        _mnemonic = data?.UserMnemonic ?? string.Empty;
        _explanation = data?.UserExplanation ?? string.Empty;
        _explanationLong = data?.UserExplanationLong ?? string.Empty;

        Answer = new WritableStringValue(
            () => _answer,
            value => _guard.Update(() => { _answer = value; Answer!.NotifyChanged(); }));
        Mnemonic = new WritableStringValue(
            () => _mnemonic,
            value => _guard.Update(() => _mnemonic = value));
        Explanation = new WritableStringValue(
            () => _explanation,
            value => _guard.Update(() => _explanation = value));
        ExplanationLong = new WritableStringValue(
            () => _explanationLong,
            value => _guard.Update(() => _explanationLong = value));
    }

    public override string ToString()
    {
        return $"Answer: {Answer.Value}, Mnemonic: {Mnemonic.Value}, Explanation: {Explanation.Value}, Explanation Long: {ExplanationLong.Value}";
    }
}
