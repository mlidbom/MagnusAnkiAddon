using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.AICreatedTests.Integration;

public class When_querying_collections : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
   public class given_three_vocabs : When_querying_collections
   {
      readonly VocabNote _vocab1;
      readonly VocabNote _vocab2;

      public given_three_vocabs()
      {
         _vocab1 = CreateVocab("食べる", "to eat", "たべる");
         _vocab2 = CreateVocab("本", "book", "ほん");
         CreateVocab("走る", "to run", "はしる");
      }

      [XF] public void WithQuestion_returns_a_single_result() =>
         GetService<VocabCollection>().WithQuestion("本").Count.Must().Be(1);

      [XF] public void WithQuestion_finds_the_matching_vocab() =>
         GetService<VocabCollection>().WithQuestion("本")[0].Must().Be(_vocab2);

      [XF] public void WithQuestion_returns_empty_for_a_nonexistent_question() =>
         GetService<VocabCollection>().WithQuestion("存在しない").Must().BeEmpty();

      [XF] public void WithIdOrNone_returns_the_correct_note() =>
         GetService<VocabCollection>().WithIdOrNone(_vocab1.GetId()).Must().Be(_vocab1);
   }

   public class given_a_vocab_with_a_form_added : When_querying_collections
   {
      public given_a_vocab_with_a_form_added()
      {
         var vocab = CreateVocab("食べる", "to eat", "たべる");
         vocab.Forms.Add("食う");
      }

      [XF] public void WithQuestion_does_not_find_by_form_value() =>
         GetService<VocabCollection>().WithQuestion("食う").Must().BeEmpty();
   }

   public class given_two_kanji : When_querying_collections
   {
      readonly KanjiNote _kanji1;

      public given_two_kanji()
      {
         _kanji1 = CreateKanji("食", "eat", "ショク", "た");
         CreateKanji("本", "book", "ホン", "もと");
      }

      [XF] public void WithKanji_finds_the_matching_kanji() =>
         GetService<KanjiCollection>().WithKanji("食").Must().Be(_kanji1);

      [XF] public void WithKanji_returns_null_for_a_nonexistent_character() =>
         GetService<KanjiCollection>().WithKanji("存").Must().BeNull();
   }

   public class given_a_sentence : When_querying_collections
   {
      readonly SentenceNote _sentence;

      public given_a_sentence() => _sentence = CreateTestSentence("これは本です。", "This is a book.");

      [XF] public void All_contains_the_sentence() =>
         GetService<SentenceCollection>().All().Must().Contain(_sentence);
   }

   public class given_one_of_each_note_type : When_querying_collections
   {
      public given_one_of_each_note_type()
      {
         CreateKanji("食", "eat", "ショク", "た");
         CreateVocab("食べる", "to eat", "たべる");
         CreateTestSentence("食べる", "to eat");
      }

      [XF] public void the_kanji_collection_has_one_note() =>
         GetService<KanjiCollection>().All().Count.Must().Be(1);

      [XF] public void the_vocab_collection_has_one_note() =>
         GetService<VocabCollection>().All().Count.Must().Be(1);

      [XF] public void the_sentence_collection_has_one_note() =>
         GetService<SentenceCollection>().All().Count.Must().Be(1);
   }
}
