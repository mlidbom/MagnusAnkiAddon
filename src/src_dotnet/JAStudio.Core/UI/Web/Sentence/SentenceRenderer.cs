using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.UI.Web.Sentence;

public static class SentenceRenderer
{
    private static string RenderWbr(string question)
    {
        if (App.Config().ShowSentenceBreakdownInEditMode.GetValue())
        {
            return question.Replace(SentenceQuestionField.WordBreakTag, "<span class='wbr_tag'>&lt;wbr&gt;</span>");
        }
        return question;
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
