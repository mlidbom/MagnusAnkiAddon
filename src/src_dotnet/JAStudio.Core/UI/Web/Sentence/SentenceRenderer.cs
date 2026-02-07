using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.UI.Web.Sentence;

public class SentenceRenderer
{
    readonly JapaneseConfig _config;
   internal SentenceRenderer(JapaneseConfig config) => _config = config;

    private string RenderWbr(string question)
    {
        if (_config.ShowSentenceBreakdownInEditMode.GetValue())
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
