using System;
using System.IO;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Storage.Media;
using Xunit;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.Storage.Media;

public class When_storing_a_media_file : IDisposable
{
   readonly string _tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");
   readonly string _mediaRoot;
   readonly MediaFileIndex _index;
   protected MediaStorageService _service = null!;

   public When_storing_a_media_file()
   {
      Directory.CreateDirectory(_tempDir);
      _mediaRoot = Path.Combine(_tempDir, "media");
      _index = new MediaFileIndex(_mediaRoot);
   }

   public void Dispose() => Directory.Delete(_tempDir, recursive: true);

   protected string CreateSourceFile(string content = "fake audio content")
   {
      var sourceDir = Path.Combine(_tempDir, "source");
      Directory.CreateDirectory(sourceDir);
      var path = Path.Combine(sourceDir, "test.mp3");
      File.WriteAllText(path, content);
      return path;
   }

   protected void InitService(MediaRoutingConfig config) =>
      _service = new MediaStorageService(_mediaRoot, _index, config);

   public class with_a_matching_routing_rule : When_storing_a_media_file
   {
      readonly MediaFileId _id;
      readonly string? _resolved;

      public with_a_matching_routing_rule()
      {
         var config = new MediaRoutingConfig(
            [new MediaRoutingRule(SourceTag.Parse("anime::natsume"), "commercial-001")]);
         InitService(config);

         var sourceFile = CreateSourceFile();
         _id = _service.StoreFile(sourceFile, SourceTag.Parse("anime::natsume::s1::01"), "natsume_ep01_03m22s.mp3",
            new NoteId(Guid.NewGuid()), MediaType.Audio, CopyrightStatus.Commercial);
         _resolved = _service.TryResolve(_id);
      }

      [XF] public void the_id_is_not_empty() => _id.IsEmpty.Must().BeFalse();
      [XF] public void the_file_is_resolvable() => _resolved.Must().NotBeNull();
      [XF] public void the_file_exists_on_disk() => File.Exists(_resolved!).Must().BeTrue();
      [XF] public void the_path_contains_the_routed_directory() => _resolved!.Must().Contain("commercial-001");
      [XF] public void the_path_uses_guid_bucket() => _resolved!.Must().Contain(Path.DirectorySeparatorChar + _id.ToString()[..2] + Path.DirectorySeparatorChar);
      [XF] public void the_file_ends_with_the_guid() => _resolved!.Must().EndWith($"{_id}.mp3");
      [XF] public void a_sidecar_file_is_written() => File.Exists(SidecarSerializer.BuildAudioSidecarPath(_resolved!)).Must().BeTrue();
   }

   public class with_no_matching_routing_rule : When_storing_a_media_file
   {
      public with_no_matching_routing_rule()
      {
         var config = new MediaRoutingConfig([new MediaRoutingRule(SourceTag.Parse("anime"), "commercial-001")]);
         InitService(config);
      }

      [XF] public void it_throws() => Assert.Throws<InvalidOperationException>(() =>
         _service.StoreFile(CreateSourceFile(), SourceTag.Parse("forvo"), "走る_forvo.mp3",
            new NoteId(Guid.NewGuid()), MediaType.Audio, CopyrightStatus.Free));
   }

   public class after_storing_a_file : When_storing_a_media_file
   {
      readonly MediaFileId _storedId;

      public after_storing_a_file()
      {
         var config = new MediaRoutingConfig([new MediaRoutingRule(SourceTag.Parse("test"), "general")]);
         InitService(config);

         var sourceFile = CreateSourceFile();
         _storedId = _service.StoreFile(sourceFile, SourceTag.Parse("test"), "test.mp3",
            new NoteId(Guid.NewGuid()), MediaType.Audio, CopyrightStatus.Free);
      }

      [XF] public void stored_file_exists() => _service.Exists(_storedId).Must().BeTrue();
      [XF] public void unknown_id_does_not_exist() => _service.Exists(MediaFileId.New()).Must().BeFalse();
   }

   public class when_rebuilding_the_index_from_filesystem : When_storing_a_media_file
   {
      readonly MediaFileId _id;
      readonly MediaFileIndex _freshIndex;

      public when_rebuilding_the_index_from_filesystem()
      {
         var config = new MediaRoutingConfig([new MediaRoutingRule(SourceTag.Parse("anime"), "general")]);
         InitService(config);

         var sourceFile = CreateSourceFile();
         _id = _service.StoreFile(sourceFile, SourceTag.Parse("anime::natsume::s1::01"), "ep01.mp3",
            new NoteId(Guid.NewGuid()), MediaType.Audio, CopyrightStatus.Commercial);

         _freshIndex = new MediaFileIndex(_mediaRoot);
         _freshIndex.Build();
      }

      [XF] public void the_fresh_index_finds_the_file() => _freshIndex.Contains(_id).Must().BeTrue();
      [XF] public void the_original_filename_is_recoverable() => _freshIndex.TryGetInfo(_id)!.OriginalFileName.Must().Be("ep01.mp3");
      [XF] public void the_sidecar_is_readable() => _freshIndex.TryGetAttachment(_id).Must().NotBeNull();
      [XF] public void the_copyright_is_preserved() => _freshIndex.TryGetAttachment(_id)!.Copyright.Must().Be(CopyrightStatus.Commercial);
   }
}
