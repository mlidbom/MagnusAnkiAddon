using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.AICreatedTests.Integration;

public class When_managing_tags : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
   public class given_a_vocab_tagged_with_TTSAudio : When_managing_tags
   {
      readonly VocabNote _vocab;

      public given_a_vocab_tagged_with_TTSAudio()
      {
         _vocab = CreateVocab("食べる", "to eat", "たべる");
         _vocab.Tags.Set(Tags.TTSAudio);
      }

      [XF] public void the_note_contains_the_tag() => _vocab.Tags.Contains(Tags.TTSAudio).Must().BeTrue();

      public class after_unsetting_the_tag : given_a_vocab_tagged_with_TTSAudio
      {
         public after_unsetting_the_tag() => _vocab.Tags.Unset(Tags.TTSAudio);

         [XF] public void the_note_no_longer_contains_the_tag() =>
            _vocab.Tags.Contains(Tags.TTSAudio).Must().BeFalse();
      }
   }

   public class given_a_kanji_with_multiple_tags : When_managing_tags
   {
      readonly KanjiNote _kanji;

      public given_a_kanji_with_multiple_tags()
      {
         _kanji = CreateKanji("食", "eat", "ショク", "た");
         _kanji.Tags.Set(Tags.TTSAudio);
         _kanji.Tags.Set(Tags.Kanji.IsRadical);
         _kanji.Tags.Set(Tags.Kanji.InVocabMainForm);
      }

      [XF] public void the_TTSAudio_tag_is_present() => _kanji.Tags.Contains(Tags.TTSAudio).Must().BeTrue();
      [XF] public void the_IsRadical_tag_is_present() => _kanji.Tags.Contains(Tags.Kanji.IsRadical).Must().BeTrue();
      [XF] public void the_InVocabMainForm_tag_is_present() => _kanji.Tags.Contains(Tags.Kanji.InVocabMainForm).Must().BeTrue();
   }

   public class given_two_vocabs_where_only_one_is_tagged : When_managing_tags
   {
      readonly VocabNote _tagged;
      readonly VocabNote _untagged;

      public given_two_vocabs_where_only_one_is_tagged()
      {
         _tagged = CreateVocab("食べる", "to eat", "たべる");
         _untagged = CreateVocab("飲む", "to drink", "のむ");
         _tagged.Tags.Set(Tags.TTSAudio);
      }

      [XF] public void the_tagged_vocab_contains_the_tag() => _tagged.Tags.Contains(Tags.TTSAudio).Must().BeTrue();
      [XF] public void the_untagged_vocab_does_not_contain_the_tag() => _untagged.Tags.Contains(Tags.TTSAudio).Must().BeFalse();
   }

   public class given_a_sentence_tagged_with_TTSAudio : When_managing_tags
   {
      readonly SentenceNote _sentence;

      public given_a_sentence_tagged_with_TTSAudio()
      {
         _sentence = CreateTestSentence("これは本です。", "This is a book.");
         _sentence.Tags.Set(Tags.TTSAudio);
      }

      [XF] public void the_tag_is_present() => _sentence.Tags.Contains(Tags.TTSAudio).Must().BeTrue();

      public class after_unsetting_the_tag : given_a_sentence_tagged_with_TTSAudio
      {
         public after_unsetting_the_tag() => _sentence.Tags.Unset(Tags.TTSAudio);

         [XF] public void the_tag_is_not_present() => _sentence.Tags.Contains(Tags.TTSAudio).Must().BeFalse();

         public class after_setting_it_again : after_unsetting_the_tag
         {
            public after_setting_it_again() => _sentence.Tags.Set(Tags.TTSAudio);

            [XF] public void the_tag_is_present_again() => _sentence.Tags.Contains(Tags.TTSAudio).Must().BeTrue();
         }
      }
   }
}
