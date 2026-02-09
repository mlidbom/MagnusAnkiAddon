using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.ReactiveProperties;

namespace JAStudio.Core.UI.Web.Sentence;

public class QuestionRenderer
{
    readonly JapaneseConfig _config;
   internal QuestionRenderer(JapaneseConfig config) => _config = config;

    public string RenderWbr(string question)
    {
        return _config.ShowSentenceBreakdownInEditMode.GetValue()
            ? question.Replace(SentenceQuestionProperty.WordBreakTag, "<span class='wbr_tag'>&lt;wbr&gt;</span>")
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
