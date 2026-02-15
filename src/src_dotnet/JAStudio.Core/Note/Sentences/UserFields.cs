using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Sentences;

public class SentenceUserFields
{
    readonly NoteGuard _guard;
    string _comments;
    string _answer;
    string _question;

    public WritableStringValue Comments { get; }
    public WritableStringValue Answer { get; }
    public WritableStringValue Question { get; }

    public SentenceUserFields(SentenceData? data, NoteGuard guard)
    {
        _guard = guard;
        _comments = data?.UserComments ?? string.Empty;
        _answer = data?.UserAnswer ?? string.Empty;
        _question = data?.UserQuestion ?? string.Empty;

        Comments = new WritableStringValue(
            () => _comments,
            value => _guard.Update(() => _comments = value));
        Answer = new WritableStringValue(
            () => _answer,
            value => _guard.Update(() => _answer = value));
        Question = new WritableStringValue(
            () => _question,
            value => _guard.Update(() => _question = value));
    }
}
