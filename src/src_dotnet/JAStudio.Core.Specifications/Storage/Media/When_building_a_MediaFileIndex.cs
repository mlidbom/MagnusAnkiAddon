using System;
using System.IO;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Note;
using JAStudio.Core.Storage.Media;
using JAStudio.Core.TaskRunners;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Specifications.Storage.Media;

public class When_building_a_MediaFileIndex : SpecificationStartingWithAnEmptyCollection
{
   readonly string _tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");
   readonly MediaFileIndex _index;

   public When_building_a_MediaFileIndex()
   {
      Directory.CreateDirectory(_tempDir);
      _index = new MediaFileIndex(_tempDir, GetService<TaskRunner>(), GetService<BackgroundTaskManager>());
   }

   public new void Dispose()
   {
      base.Dispose();
      Directory.Delete(_tempDir, recursive: true);
   }

   static void CreateMediaFileWithSidecar(string dir, MediaFileId id, string originalFileName, NoteId noteId, CopyrightStatus copyright = CopyrightStatus.Free)
   {
      Directory.CreateDirectory(dir);
      var extension = Path.GetExtension(originalFileName);
      var mediaPath = Path.Combine(dir, $"{id}{extension}");
      File.WriteAllText(mediaPath, "fake audio");

      var audio = new AudioAttachment
                  {
                     Id = id,
                     NoteIds = [noteId],
                     NoteSourceTag = SourceTag.Parse("source::test"),
                     OriginalFileName = originalFileName,
                     Copyright = copyright
                  };
      SidecarSerializer.WriteAudioSidecar(SidecarSerializer.BuildAudioSidecarPath(mediaPath), audio);
   }

   public class over_a_directory_with_a_sidecar_file : When_building_a_MediaFileIndex
   {
      readonly MediaFileId _id = MediaFileId.New();
      readonly NoteId _noteId = new(Guid.NewGuid());

      public over_a_directory_with_a_sidecar_file()
      {
         var fileDir = Path.Combine(_tempDir, "anime", "natsume", "a1");
         CreateMediaFileWithSidecar(fileDir, _id, "natsume_ep01_03m22s.mp3", _noteId, CopyrightStatus.Commercial);
         _index.Build();
      }

      [XF] public void it_indexes_the_file() => _index.Count.Must().Be(1);
      [XF] public void it_contains_the_id() => _index.Contains(_id).Must().BeTrue();

      public class and_resolving_by_id : over_a_directory_with_a_sidecar_file
      {
         readonly string? _resolved;
         public and_resolving_by_id() => _resolved = _index.TryResolve(_id);

         [XF] public void it_returns_the_full_path() => _resolved.Must().NotBeNull();
         [XF] public void the_path_points_to_an_existing_file() => File.Exists(_resolved!).Must().BeTrue();
      }

      public class and_getting_file_info : over_a_directory_with_a_sidecar_file
      {
         readonly MediaFileInfo? _info;
         public and_getting_file_info() => _info = _index.TryGetInfo(_id);

         [XF] public void it_returns_info() => _info.Must().NotBeNull();
         [XF] public void the_original_filename_comes_from_sidecar() => _info!.OriginalFileName.Must().Be("natsume_ep01_03m22s.mp3");
         [XF] public void the_extension_is_extracted() => _info!.Extension.Must().Be(".mp3");
      }

      public class and_getting_attachment : over_a_directory_with_a_sidecar_file
      {
         readonly MediaAttachment? _attachment;
         public and_getting_attachment() => _attachment = _index.TryGetAttachment(_id);

         [XF] public void it_returns_an_audio_attachment() => (_attachment is AudioAttachment).Must().BeTrue();
         [XF] public void it_has_the_correct_copyright() => _attachment!.Copyright.Must().Be(CopyrightStatus.Commercial);
         [XF] public void it_has_the_correct_note_id() => _attachment!.NoteIds[0].Must().Be(_noteId);
      }

      public class and_querying_by_note_id : over_a_directory_with_a_sidecar_file
      {
         readonly NoteMedia _noteMedia;
         public and_querying_by_note_id() => _noteMedia = _index.GetNoteMedia(_noteId);

         [XF] public void it_returns_one_audio() => _noteMedia.Audio.Count.Must().Be(1);
         [XF] public void it_returns_no_images() => _noteMedia.Images.Count.Must().Be(0);
      }
   }

   public class over_a_directory_with_no_sidecars : When_building_a_MediaFileIndex
   {
      public over_a_directory_with_no_sidecars()
      {
         var fileDir = Path.Combine(_tempDir, "some", "path");
         Directory.CreateDirectory(fileDir);
         File.WriteAllText(Path.Combine(fileDir, "not-a-guid.mp3"), "fake audio");
         File.WriteAllText(Path.Combine(fileDir, "readme.txt"), "some text");
         _index.Build();
      }

      [XF] public void it_indexes_nothing() => _index.Count.Must().Be(0);
   }

   public class over_a_nonexistent_directory : When_building_a_MediaFileIndex
   {
      readonly MediaFileIndex _nonexistentIndex;

      public over_a_nonexistent_directory()
      {
         _nonexistentIndex = new MediaFileIndex(Path.Combine(_tempDir, "does_not_exist"), GetService<TaskRunner>(), GetService<BackgroundTaskManager>());
         _nonexistentIndex.Build();
      }

      [XF] public void it_indexes_nothing() => _nonexistentIndex.Count.Must().Be(0);
   }

   public class without_explicit_Build_call : When_building_a_MediaFileIndex
   {
      readonly MediaFileId _id = MediaFileId.New();

      public without_explicit_Build_call()
      {
         var fileDir = Path.Combine(_tempDir, "a1");
         CreateMediaFileWithSidecar(fileDir, _id, "test.mp3", new NoteId(Guid.NewGuid()));
      }

      [XF] public void it_lazy_initializes_on_first_access() => _index.Contains(_id).Must().BeTrue();
   }

   public class resolving_an_unknown_id : When_building_a_MediaFileIndex
   {
      public resolving_an_unknown_id() => _index.Build();

      [XF] public void it_returns_null() => _index.TryResolve(MediaFileId.New()).Must().BeNull();
   }

   public class querying_note_media_for_unknown_note : When_building_a_MediaFileIndex
   {
      public querying_note_media_for_unknown_note() => _index.Build();

      [XF] public void it_returns_empty_note_media() => _index.GetNoteMedia(new NoteId(Guid.NewGuid())).Audio.Count.Must().Be(0);
   }
}
