using System;
using System.IO;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Storage.Media;

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
            [new MediaRoutingRule("anime::natsume", "commercial-001")],
            "general");
         InitService(config);

         var sourceFile = CreateSourceFile();
         _id = _service.StoreFile(sourceFile, "anime::natsume::s1::01", "natsume_ep01_03m22s.mp3");
         _resolved = _service.TryResolve(_id);
      }

      [XF] public void the_id_is_not_empty() => _id.IsEmpty.Must().BeFalse();
      [XF] public void the_file_is_resolvable() => _resolved.Must().NotBeNull();
      [XF] public void the_file_exists_on_disk() => File.Exists(_resolved!).Must().BeTrue();
      [XF] public void the_path_contains_the_routed_directory() => _resolved!.Must().Contain("commercial-001");
      [XF] public void the_path_contains_the_source_tag_hierarchy() => _resolved!.Must().Contain(Path.Combine("anime", "natsume", "s1", "01"));
      [XF] public void the_path_contains_the_original_filename() => _resolved!.Must().Contain("natsume_ep01_03m22s.mp3");
      [XF] public void the_file_ends_with_the_guid() => _resolved!.Must().EndWith($"{_id}.mp3");
   }

   public class with_default_routing : When_storing_a_media_file
   {
      readonly string? _resolved;

      public with_default_routing()
      {
         var config = MediaRoutingConfig.Default();
         InitService(config);

         var sourceFile = CreateSourceFile();
         var id = _service.StoreFile(sourceFile, "forvo", "走る_forvo.mp3");
         _resolved = _service.TryResolve(id);
      }

      [XF] public void the_path_uses_the_general_directory() => _resolved!.Must().Contain("general");
   }

   public class checking_existence : When_storing_a_media_file
   {
      readonly MediaFileId _storedId;

      public checking_existence()
      {
         var config = MediaRoutingConfig.Default();
         InitService(config);

         var sourceFile = CreateSourceFile();
         _storedId = _service.StoreFile(sourceFile, "test", "test.mp3");
      }

      [XF] public void stored_file_exists() => _service.Exists(_storedId).Must().BeTrue();
      [XF] public void unknown_id_does_not_exist() => _service.Exists(MediaFileId.New()).Must().BeFalse();
   }

   public class rebuilding_index_from_filesystem : When_storing_a_media_file
   {
      readonly MediaFileId _id;
      readonly MediaFileIndex _freshIndex;

      public rebuilding_index_from_filesystem()
      {
         var config = MediaRoutingConfig.Default();
         InitService(config);

         var sourceFile = CreateSourceFile();
         _id = _service.StoreFile(sourceFile, "anime::natsume::s1::01", "ep01.mp3");

         _freshIndex = new MediaFileIndex(_mediaRoot);
         _freshIndex.Build();
      }

      [XF] public void the_fresh_index_finds_the_file() => _freshIndex.Contains(_id).Must().BeTrue();
      [XF] public void the_original_filename_is_recoverable() => _freshIndex.TryGetInfo(_id)!.OriginalFileName.Must().Be("ep01.mp3");
   }
}
