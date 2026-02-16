using System;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Storage.Media;
using Xunit;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.Storage.Media;

public class When_configuring_media_import_routing
{
   static SourceTag Tag(string value) => SourceTag.Parse(value);

   public class with_multiple_sentence_rules : When_configuring_media_import_routing
   {
      readonly MediaImportRuleSet _ruleSet = new(
         [],
         [
            new SentenceImportRule(Tag("anime::natsume"), SentenceMediaField.Audio, "commercial-001", CopyrightStatus.Commercial),
            new SentenceImportRule(Tag("anime::natsume"), SentenceMediaField.Screenshot, "commercial-001", CopyrightStatus.Commercial),
            new SentenceImportRule(Tag("anime"), SentenceMediaField.Audio, "commercial-002", CopyrightStatus.Commercial),
            new SentenceImportRule(Tag("anime"), SentenceMediaField.Screenshot, "commercial-002", CopyrightStatus.Commercial)
         ],
         []);

      [XF] public void it_resolves_the_longest_matching_prefix() => _ruleSet.TryResolveSentence(Tag("anime::natsume::s1::01"), SentenceMediaField.Audio)!.TargetDirectory.Must().Be("commercial-001");
      [XF] public void it_falls_back_to_shorter_prefix() => _ruleSet.TryResolveSentence(Tag("anime::mushishi::s1::05"), SentenceMediaField.Audio)!.TargetDirectory.Must().Be("commercial-002");
   }

   public class with_no_matching_rule : When_configuring_media_import_routing
   {
      readonly MediaImportRuleSet _ruleSet = new(
         [],
         [new SentenceImportRule(Tag("anime"), SentenceMediaField.Audio, "commercial-001", CopyrightStatus.Commercial)],
         []);

      [XF] public void it_returns_null() => _ruleSet.TryResolveSentence(Tag("forvo"), SentenceMediaField.Audio).Must().BeNull();
   }

   public class with_vocab_rules_having_different_copyright_per_field : When_configuring_media_import_routing
   {
      readonly MediaImportRuleSet _ruleSet;

      public with_vocab_rules_having_different_copyright_per_field()
      {
         _ruleSet = new MediaImportRuleSet(
            [
               new VocabImportRule(Tag("wani"), VocabMediaField.AudioFirst, "commercial/wani", CopyrightStatus.Commercial),
               new VocabImportRule(Tag("wani"), VocabMediaField.AudioTts, "free/tts", CopyrightStatus.Free),
               new VocabImportRule(Tag("wani"), VocabMediaField.UserImage, "free/user", CopyrightStatus.Free)
            ],
            [],
            []);
      }

      [XF] public void audio_first_is_commercial() => _ruleSet.TryResolveVocab(Tag("wani::level05"), VocabMediaField.AudioFirst)!.Copyright.Must().Be(CopyrightStatus.Commercial);
      [XF] public void audio_tts_is_free() => _ruleSet.TryResolveVocab(Tag("wani::level05"), VocabMediaField.AudioTts)!.Copyright.Must().Be(CopyrightStatus.Free);
      [XF] public void audio_first_goes_to_commercial_dir() => _ruleSet.TryResolveVocab(Tag("wani::level05"), VocabMediaField.AudioFirst)!.TargetDirectory.Must().Be("commercial/wani");
      [XF] public void audio_tts_goes_to_free_dir() => _ruleSet.TryResolveVocab(Tag("wani::level05"), VocabMediaField.AudioTts)!.TargetDirectory.Must().Be("free/tts");
      [XF] public void user_image_is_free() => _ruleSet.TryResolveVocab(Tag("wani::level05"), VocabMediaField.UserImage)!.Copyright.Must().Be(CopyrightStatus.Free);
      [XF] public void unconfigured_field_returns_null() => _ruleSet.TryResolveVocab(Tag("wani::level05"), VocabMediaField.AudioSecond).Must().BeNull();
   }
}
