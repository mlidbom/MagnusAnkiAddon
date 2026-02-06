using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.UI.Web.Sentence;

public class QuestionRenderer
{
    readonly TemporaryServiceCollection _services;
    internal QuestionRenderer(TemporaryServiceCollection services) => _services = services;

    public static string RenderWbr(string question)
    {
        return App.Config().ShowSentenceBreakdownInEditMode.GetValue()
            ? question.Replace(SentenceQuestionField.WordBreakTag, "<span class='wbr_tag'>&lt;wbr&gt;</span>")
            : question;
    }

    public static string RenderUserQuestion(SentenceNote note)
    {
        return RenderWbr(note.User.Question.Value);
    }

    public static string RenderSourceQuestion(SentenceNote note)
    {
        return RenderWbr(note.SourceQuestion.Value);
    }
}
