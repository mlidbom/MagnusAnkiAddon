using System;
using System.Collections.Generic;
using System.IO;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Note;
using JAStudio.Core.Storage.Media;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.Storage.Media;

public class When_serializing_a_sidecar
{
   public class for_an_audio_attachment : When_serializing_a_sidecar
   {
      readonly AudioAttachment _original;
      readonly AudioAttachment _deserialized;
      readonly string _json;

      public for_an_audio_attachment()
      {
         _original = new AudioAttachment
                     {
                        Id = new MediaFileId(Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890")),
                        NoteIds = [new NoteId(Guid.Parse("9f8e7d6c-5b4a-3210-fedc-ba9876543210"))],
                        NoteSourceTag = "source::anime::natsume::s1::01",
                        AnkiFieldName = "Audio",
                        OriginalFileName = "natsume_ep01_03m22s.mp3",
                        Copyright = CopyrightStatus.Commercial
                     };

         _json = SidecarSerializer.SerializeAudio(_original);
         _deserialized = SidecarSerializer.DeserializeAudio(_json);
      }

      [XF] public void it_roundtrips_the_id() => _deserialized.Id.Must().Be(_original.Id);
      [XF] public void it_roundtrips_the_note_ids() => _deserialized.NoteIds.Count.Must().Be(1);
      [XF] public void it_roundtrips_the_note_source_tag() => _deserialized.NoteSourceTag.Must().Be("source::anime::natsume::s1::01");
      [XF] public void it_roundtrips_the_anki_field_name() => _deserialized.AnkiFieldName.Must().Be("Audio");
      [XF] public void it_roundtrips_the_original_filename() => _deserialized.OriginalFileName.Must().Be("natsume_ep01_03m22s.mp3");
      [XF] public void it_roundtrips_the_copyright() => _deserialized.Copyright.Must().Be(CopyrightStatus.Commercial);
      [XF] public void tts_is_null_when_not_set() => _deserialized.Tts.Must().BeNull();
      [XF] public void the_json_contains_camelCase_properties() => _json.Must().Contain("\"noteIds\"");
      [XF] public void the_json_does_not_contain_filePath() => _json.Must().NotContain("filePath");
   }

   public class for_an_audio_attachment_with_tts : When_serializing_a_sidecar
   {
      readonly AudioAttachment _original;
      readonly AudioAttachment _deserialized;

      public for_an_audio_attachment_with_tts()
      {
         _original = new AudioAttachment
                     {
                        Id = new MediaFileId(Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890")),
                        NoteIds = [new NoteId(Guid.Parse("9f8e7d6c-5b4a-3210-fedc-ba9876543210"))],
                        NoteSourceTag = "source::wani::level05",
                        AnkiFieldName = "Audio",
                        Copyright = CopyrightStatus.Free,
                        Tts = new TtsInfo("azure-neural", "ja-JP-NanamiNeural", "2025.1")
                     };

         var json = SidecarSerializer.SerializeAudio(_original);
         _deserialized = SidecarSerializer.DeserializeAudio(json);
      }

      [XF] public void it_roundtrips_the_tts_engine() => _deserialized.Tts!.Engine.Must().Be("azure-neural");
      [XF] public void it_roundtrips_the_tts_voice() => _deserialized.Tts!.Voice.Must().Be("ja-JP-NanamiNeural");
      [XF] public void it_roundtrips_the_tts_version() => _deserialized.Tts!.Version.Must().Be("2025.1");
      [XF] public void it_roundtrips_the_copyright_as_free() => _deserialized.Copyright.Must().Be(CopyrightStatus.Free);
   }

   public class for_an_audio_attachment_with_multiple_note_ids : When_serializing_a_sidecar
   {
      readonly AudioAttachment _deserialized;

      public for_an_audio_attachment_with_multiple_note_ids()
      {
         var attachment = new AudioAttachment
                          {
                             Id = MediaFileId.New(),
                             NoteIds =
                             [
                                new NoteId(Guid.Parse("11111111-1111-1111-1111-111111111111")),
                                new NoteId(Guid.Parse("22222222-2222-2222-2222-222222222222")),
                                new NoteId(Guid.Parse("33333333-3333-3333-3333-333333333333"))
                             ],
                             NoteSourceTag = "source::core2000::step01",
                             AnkiFieldName = "Audio.First",
                             OriginalFileName = "走る_core2k.mp3",
                             Copyright = CopyrightStatus.Commercial
                          };

         var json = SidecarSerializer.SerializeAudio(attachment);
         _deserialized = SidecarSerializer.DeserializeAudio(json);
      }

      [XF] public void it_preserves_all_note_ids() => _deserialized.NoteIds.Count.Must().Be(3);
   }

   public class for_an_image_attachment : When_serializing_a_sidecar
   {
      readonly ImageAttachment _original;
      readonly ImageAttachment _deserialized;

      public for_an_image_attachment()
      {
         _original = new ImageAttachment
                     {
                        Id = new MediaFileId(Guid.Parse("f7e6d5c4-b3a2-1098-7654-321fedcba098")),
                        NoteIds = [new NoteId(Guid.Parse("9f8e7d6c-5b4a-3210-fedc-ba9876543210"))],
                        NoteSourceTag = "source::anime::natsume::s1::01",
                        AnkiFieldName = "Screenshot",
                        OriginalFileName = "natsume_ep01_03m22s.png",
                        Copyright = CopyrightStatus.Commercial
                     };

         var json = SidecarSerializer.SerializeImage(_original);
         _deserialized = SidecarSerializer.DeserializeImage(json);
      }

      [XF] public void it_roundtrips_the_id() => _deserialized.Id.Must().Be(_original.Id);
      [XF] public void it_roundtrips_the_copyright() => _deserialized.Copyright.Must().Be(CopyrightStatus.Commercial);
      [XF] public void it_roundtrips_the_original_filename() => _deserialized.OriginalFileName.Must().Be("natsume_ep01_03m22s.png");
   }

   public class omitting_default_values : When_serializing_a_sidecar
   {
      readonly string _json;

      public omitting_default_values()
      {
         var attachment = new AudioAttachment
                          {
                             Id = MediaFileId.New(),
                             NoteIds = [new NoteId(Guid.NewGuid())],
                             NoteSourceTag = "source::wani::level05",
                             Copyright = CopyrightStatus.Free
                          };

         _json = SidecarSerializer.SerializeAudio(attachment);
      }

      [XF] public void it_omits_null_originalFileName() => _json.Must().NotContain("originalFileName");
      [XF] public void it_omits_null_ankiFieldName() => _json.Must().NotContain("ankiFieldName");
      [XF] public void it_omits_null_tts() => _json.Must().NotContain("tts");
   }

   public class writing_and_reading_files : When_serializing_a_sidecar, IDisposable
   {
      readonly string _tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");

      public writing_and_reading_files() => Directory.CreateDirectory(_tempDir);

      public void Dispose() => Directory.Delete(_tempDir, recursive: true);

      public class audio_sidecar_file : writing_and_reading_files
      {
         readonly AudioAttachment _read;

         public audio_sidecar_file()
         {
            var attachment = new AudioAttachment
                             {
                                Id = new MediaFileId(Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890")),
                                NoteIds = [new NoteId(Guid.NewGuid())],
                                NoteSourceTag = "source::test",
                                Copyright = CopyrightStatus.Free
                             };

            var mediaFilePath = Path.Combine(_tempDir, "a1b2c3d4-e5f6-7890-abcd-ef1234567890.mp3");
            var sidecarPath = SidecarSerializer.BuildAudioSidecarPath(mediaFilePath);
            SidecarSerializer.WriteAudioSidecar(sidecarPath, attachment);
            _read = SidecarSerializer.ReadAudioSidecar(sidecarPath);
         }

         [XF] public void it_roundtrips_through_file() => _read.Id.Must().Be(new MediaFileId(Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890")));
         [XF] public void the_sidecar_has_audio_json_extension() =>
            SidecarSerializer.BuildAudioSidecarPath("dir/a1b2c3d4.mp3").Must().EndWith(".audio.json");
      }

      public class image_sidecar_file : writing_and_reading_files
      {
         readonly ImageAttachment _read;

         public image_sidecar_file()
         {
            var attachment = new ImageAttachment
                             {
                                Id = new MediaFileId(Guid.Parse("f7e6d5c4-b3a2-1098-7654-321fedcba098")),
                                NoteIds = [new NoteId(Guid.NewGuid())],
                                NoteSourceTag = "source::test",
                                Copyright = CopyrightStatus.Commercial
                             };

            var mediaFilePath = Path.Combine(_tempDir, "f7e6d5c4-b3a2-1098-7654-321fedcba098.png");
            var sidecarPath = SidecarSerializer.BuildImageSidecarPath(mediaFilePath);
            SidecarSerializer.WriteImageSidecar(sidecarPath, attachment);
            _read = SidecarSerializer.ReadImageSidecar(sidecarPath);
         }

         [XF] public void it_roundtrips_through_file() => _read.Id.Must().Be(new MediaFileId(Guid.Parse("f7e6d5c4-b3a2-1098-7654-321fedcba098")));
         [XF] public void the_sidecar_has_image_json_extension() =>
            SidecarSerializer.BuildImageSidecarPath("dir/f7e6d5c4.png").Must().EndWith(".image.json");
      }
   }
}
