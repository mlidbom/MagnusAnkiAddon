using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Sentences;

public class SentenceUserFields
{
    public WritableStringValue Comments { get; }
    public WritableStringValue Answer { get; }
    public WritableStringValue Question { get; }

    public SentenceUserFields(SentenceData? data, NoteGuard guard)
    {
        Comments = new WritableStringValue(data?.UserComments ?? string.Empty, guard);
        Answer = new WritableStringValue(data?.UserAnswer ?? string.Empty, guard);
        Question = new WritableStringValue(data?.UserQuestion ?? string.Empty, guard);
    }
}
