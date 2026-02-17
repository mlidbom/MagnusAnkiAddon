using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.Sentences;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.AICreatedTests.Integration.When_querying_collections;

public class for_sentences : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
   public class given_a_sentence : for_sentences
   {
      readonly SentenceNote _sentence;

      public given_a_sentence() => _sentence = CreateTestSentence("これは本です。", "This is a book.");

      [XF] public void All_contains_the_sentence() =>
         GetService<SentenceCollection>().All().Must().Contain(_sentence);
   }
}
