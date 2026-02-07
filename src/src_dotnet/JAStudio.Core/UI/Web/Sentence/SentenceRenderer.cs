using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.UI.Web.Sentence;

public class SentenceRenderer
{
    readonly TemporaryServiceCollection _services;
    internal SentenceRenderer(TemporaryServiceCollection services) => _services = services;

    private string RenderWbr(string question)
    {
        if (TemporaryServiceCollection.Instance.App.Config().ShowSentenceBreakdownInEditMode.GetValue())
        {
            return question.Replace(SentenceQuestionField.WordBreakTag, "<span class='wbr_tag'>&lt;wbr&gt;</span>");
        }
        return question;
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
