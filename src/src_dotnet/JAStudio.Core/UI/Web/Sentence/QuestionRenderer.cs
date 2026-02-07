using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.UI.Web.Sentence;

public class QuestionRenderer
{
    readonly TemporaryServiceCollection _services;
    internal QuestionRenderer(TemporaryServiceCollection services) => _services = services;

    public string RenderWbr(string question)
    {
        return TemporaryServiceCollection.Instance.App.Config().ShowSentenceBreakdownInEditMode.GetValue()
            ? question.Replace(SentenceQuestionField.WordBreakTag, "<span class='wbr_tag'>&lt;wbr&gt;</span>")
            : question;
    }

    public string RenderUserQuestion(SentenceNote note)
    {
        return RenderWbr(note.User.Question.Value);
    }

    public string RenderSourceQuestion(SentenceNote note)
    {
        return RenderWbr(note.SourceQuestion.Value);
    }
}
