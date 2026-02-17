using JAStudio.Core.Configuration;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Sentences;

namespace JAStudio.Core.UI.Web.Sentence;

class QuestionRenderer
{
   readonly JapaneseConfig _config;
   internal QuestionRenderer(JapaneseConfig config) => _config = config;

   public string RenderWbr(string question) =>
      _config.ShowSentenceBreakdownInEditMode.Value
         ? question.Replace(SentenceQuestionField.WordBreakTag, "<span class='wbr_tag'>&lt;wbr&gt;</span>")
         : question;

   public string RenderUserQuestion(SentenceNote note) => RenderWbr(note.User.Question.Value);

   public string RenderSourceQuestion(SentenceNote note) => RenderWbr(note.SourceQuestion.Value);
}
