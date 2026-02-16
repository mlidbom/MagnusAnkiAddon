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
   static MediaImportRoute Route(string dir, CopyrightStatus c = CopyrightStatus.Commercial) => new(dir, c);

   public class with_multiple_sentence_rules : When_configuring_media_import_routing
   {
      readonly MediaImportRoutingConfig<SentenceMediaImportRule> _config = new(
         [
            new SentenceMediaImportRule(Tag("anime::natsume"), Route("commercial-001"), Route("commercial-001")),
            new SentenceMediaImportRule(Tag("anime"), Route("commercial-002"), Route("commercial-002"))
         ]);

      [XF] public void it_resolves_the_longest_matching_prefix() => _config.Resolve(Tag("anime::natsume::s1::01")).Audio.TargetDirectory.Must().Be("commercial-001");
      [XF] public void it_falls_back_to_shorter_prefix() => _config.Resolve(Tag("anime::mushishi::s1::05")).Audio.TargetDirectory.Must().Be("commercial-002");
   }

   public class with_no_matching_rule : When_configuring_media_import_routing
   {
      readonly MediaImportRoutingConfig<SentenceMediaImportRule> _config = new(
         [new SentenceMediaImportRule(Tag("anime"), Route("commercial-001"), Route("commercial-001"))]);

      [XF] public void it_throws() => Assert.Throws<InvalidOperationException>(() => _config.Resolve(Tag("forvo")));
   }

   public class with_vocab_rules_having_different_copyright_per_field : When_configuring_media_import_routing
   {
      readonly VocabMediaImportRule _resolved;

      public with_vocab_rules_having_different_copyright_per_field()
      {
         var config = new MediaImportRoutingConfig<VocabMediaImportRule>(
            [
               new VocabMediaImportRule(
                  Tag("wani"),
                  AudioFirst: Route("commercial/wani"),
                  AudioSecond: Route("commercial/wani"),
                  AudioTts: Route("free/tts", CopyrightStatus.Free),
                  Image: Route("commercial/wani"),
                  UserImage: Route("free/user", CopyrightStatus.Free))
            ]);

         _resolved = config.Resolve(Tag("wani::level05"));
      }

      [XF] public void audio_first_is_commercial() => _resolved.AudioFirst.Copyright.Must().Be(CopyrightStatus.Commercial);
      [XF] public void audio_tts_is_free() => _resolved.AudioTts.Copyright.Must().Be(CopyrightStatus.Free);
      [XF] public void audio_first_goes_to_commercial_dir() => _resolved.AudioFirst.TargetDirectory.Must().Be("commercial/wani");
      [XF] public void audio_tts_goes_to_free_dir() => _resolved.AudioTts.TargetDirectory.Must().Be("free/tts");
      [XF] public void user_image_is_free() => _resolved.UserImage.Copyright.Must().Be(CopyrightStatus.Free);
   }
}
