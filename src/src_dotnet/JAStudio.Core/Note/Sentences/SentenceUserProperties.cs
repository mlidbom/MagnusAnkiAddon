using JAStudio.Core.Note.ReactiveProperties;

namespace JAStudio.Core.Note.Sentences;

public class SentenceUserProperties
{
   public StringProperty Comments { get; }
   public StringProperty Answer { get; }
   public StringProperty Question { get; }

   public SentenceUserProperties(StringProperty comments, StringProperty answer, StringProperty question)
   {
      Comments = comments;
      Answer = answer;
      Question = question;
   }
}
