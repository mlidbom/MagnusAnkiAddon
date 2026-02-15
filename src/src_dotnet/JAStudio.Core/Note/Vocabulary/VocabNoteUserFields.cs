using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteUserFields
{
   public WritableStringValue Answer { get; }
   public WritableStringValue Mnemonic { get; }
   public WritableStringValue Explanation { get; }
   public WritableStringValue ExplanationLong { get; }

   public VocabNoteUserFields(VocabData? data, NoteGuard guard)
   {
      Answer = new WritableStringValue(data?.UserAnswer ?? string.Empty, guard);
      Mnemonic = new WritableStringValue(data?.UserMnemonic ?? string.Empty, guard);
      Explanation = new WritableStringValue(data?.UserExplanation ?? string.Empty, guard);
      ExplanationLong = new WritableStringValue(data?.UserExplanationLong ?? string.Empty, guard);
   }

   public override string ToString() =>
      $"Answer: {Answer.Value}, Mnemonic: {Mnemonic.Value}, Explanation: {Explanation.Value}, Explanation Long: {ExplanationLong.Value}";
}
