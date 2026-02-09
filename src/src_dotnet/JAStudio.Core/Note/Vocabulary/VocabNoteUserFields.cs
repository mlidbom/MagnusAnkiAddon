using JAStudio.Core.Note.ReactiveProperties;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteUserFields
{
    public readonly StringProperty Answer;
    public readonly StringProperty Mnemonic;
    public readonly StringProperty Explanation;
    public readonly StringProperty ExplanationLong;

    public VocabNoteUserFields(StringProperty answer, StringProperty mnemonic, StringProperty explanation, StringProperty explanationLong)
    {
        Answer = answer;
        Mnemonic = mnemonic;
        Explanation = explanation;
        ExplanationLong = explanationLong;
    }

    public override string ToString()
    {
        return $"Answer: {Answer.Value}, Mnemonic: {Mnemonic.Value}, Explanation: {Explanation.Value}, Explanation Long: {ExplanationLong.Value}";
    }
}
