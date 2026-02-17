using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.Vocabulary;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.AICreatedTests.Integration;

public class When_updating_cached_note_data : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
   public class after_changing_a_vocabs_question : When_updating_cached_note_data
   {
      readonly VocabNote _vocab;

      public after_changing_a_vocabs_question()
      {
         _vocab = CreateVocab("食べる", "to eat", "たべる");
         _vocab.GetQuestion();
         _vocab.Question.Set("飲む");
         _vocab.UpdateGeneratedData();
      }

      [XF] public void the_old_question_no_longer_finds_it() =>
         GetService<VocabCollection>().WithQuestion("食べる").Must().BeEmpty();

      [XF] public void the_new_question_finds_it() =>
         GetService<VocabCollection>().WithQuestion("飲む").Count.Must().Be(1);

      [XF] public void the_new_question_returns_the_same_note() =>
         GetService<VocabCollection>().WithQuestion("飲む")[0].Must().Be(_vocab);
   }

   public class after_adding_a_form_to_a_vocab : When_updating_cached_note_data
   {
      public after_adding_a_form_to_a_vocab()
      {
         var vocab = CreateVocab("食べる", "to eat", "たべる");
         vocab.Forms.Add("taberu-form");
      }

      [XF] public void WithQuestion_does_not_find_the_form() =>
         GetService<VocabCollection>().WithQuestion("taberu-form").Must().BeEmpty();

      [XF] public void the_original_question_still_finds_it() =>
         GetService<VocabCollection>().WithQuestion("食べる").Count.Must().Be(1);
   }

   public class after_adding_and_then_removing_a_form : When_updating_cached_note_data
   {
      readonly VocabNote _vocab;

      public after_adding_and_then_removing_a_form()
      {
         _vocab = CreateVocab("食べる", "to eat", "たべる");
         _vocab.Forms.Add("食う");
         _vocab.Forms.Remove("食う");
      }

      [XF] public void the_removed_form_is_no_longer_present() =>
         _vocab.Forms.AllSet().Contains("食う").Must().BeFalse();

      [XF] public void the_original_question_still_finds_it() =>
         GetService<VocabCollection>().WithQuestion("食べる").Count.Must().Be(1);
   }

   public class after_changing_a_kanjis_question : When_updating_cached_note_data
   {
      readonly KanjiNote _kanji;

      public after_changing_a_kanjis_question()
      {
         _kanji = CreateKanji("食", "eat", "ショク", "た");
         _kanji.SetQuestion("飲");
         _kanji.UpdateGeneratedData();
      }

      [XF] public void the_old_character_no_longer_finds_it() =>
         GetService<KanjiCollection>().WithKanji("食").Must().BeNull();

      [XF] public void the_new_character_finds_it() =>
         GetService<KanjiCollection>().WithKanji("飲").Must().Be(_kanji);
   }

   public class after_multiple_updates : When_updating_cached_note_data
   {
      readonly VocabNote _vocab;

      public after_multiple_updates()
      {
         _vocab = CreateVocab("走る", "to run", "はしる");
         _vocab.Forms.Add("駆ける");
         _vocab.Forms.Add("ダッシュする");
         _vocab.Question.Set("疾走する");
         _vocab.UpdateGeneratedData();
         _vocab.Forms.Remove("駆ける");
      }

      [XF] public void the_new_question_finds_it() =>
         GetService<VocabCollection>().WithQuestion("疾走する").Count.Must().Be(1);

      [XF] public void the_old_question_does_not_find_it() =>
         GetService<VocabCollection>().WithQuestion("走る").Must().BeEmpty();

      [XF] public void removed_forms_are_gone() =>
         _vocab.Forms.AllSet().Contains("駆ける").Must().BeFalse();

      [XF] public void surviving_forms_remain() =>
         _vocab.Forms.AllSet().Must().Contain("ダッシュする");
   }
}
