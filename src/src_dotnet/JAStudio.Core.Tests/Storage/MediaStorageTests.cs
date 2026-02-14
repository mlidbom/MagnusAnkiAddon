using System;
using System.IO;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Storage.Media;

namespace JAStudio.Core.Tests.Storage;

public class When_creating_a_MediaFileId
{
   public class via_New : When_creating_a_MediaFileId
   {
      readonly MediaFileId _id1 = MediaFileId.New();
      readonly MediaFileId _id2 = MediaFileId.New();

      [XF] public void it_is_not_empty() => _id1.IsEmpty.Must().BeFalse();
      [XF] public void each_id_is_unique() => _id1.Must().NotBe(_id2);
   }

   public class via_Parse : When_creating_a_MediaFileId
   {
      readonly MediaFileId _original = MediaFileId.New();
      readonly MediaFileId _parsed;
      public via_Parse() => _parsed = MediaFileId.Parse(_original.ToString());

      [XF] public void it_roundtrips_through_ToString() => _parsed.Must().Be(_original);
   }

   public class via_TryParse : When_creating_a_MediaFileId
   {
      public class with_a_valid_guid : via_TryParse
      {
         readonly MediaFileId _expected = MediaFileId.New();
         readonly bool _success;
         readonly MediaFileId _parsed;

         public with_a_valid_guid() => _success = MediaFileId.TryParse(_expected.ToString(), out _parsed);

         [XF] public void it_returns_true() => _success.Must().BeTrue();
         [XF] public void the_parsed_id_matches() => _parsed.Must().Be(_expected);
      }

      public class with_invalid_input : via_TryParse
      {
         [XF] public void it_returns_false_for_garbage() => MediaFileId.TryParse("not-a-guid", out _).Must().BeFalse();
         [XF] public void it_returns_false_for_null() => MediaFileId.TryParse(null, out _).Must().BeFalse();
         [XF] public void it_returns_false_for_empty() => MediaFileId.TryParse("", out _).Must().BeFalse();
      }
   }

   public class with_default_value : When_creating_a_MediaFileId
   {
      [XF] public void it_is_empty() => default(MediaFileId).IsEmpty.Must().BeTrue();
   }
}

public class When_building_a_MediaFileIndex : IDisposable
{
   readonly string _tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");
   readonly MediaFileIndex _index;

   public When_building_a_MediaFileIndex()
   {
      Directory.CreateDirectory(_tempDir);
      _index = new MediaFileIndex(_tempDir);
   }

   public void Dispose() => Directory.Delete(_tempDir, recursive: true);

   public class over_a_directory_with_guid_named_files : When_building_a_MediaFileIndex
   {
      readonly MediaFileId _id = MediaFileId.New();

      public over_a_directory_with_guid_named_files()
      {
         var fileDir = Path.Combine(_tempDir, "anime", "natsume", "natsume_ep01_03m22s.mp3");
         Directory.CreateDirectory(fileDir);
         File.WriteAllText(Path.Combine(fileDir, $"{_id}.mp3"), "fake audio");
         _index.Build();
      }

      [XF] public void it_indexes_the_file() => _index.Count.Must().Be(1);
      [XF] public void it_contains_the_id() => _index.Contains(_id).Must().BeTrue();

      public class and_resolving_by_id : over_a_directory_with_guid_named_files
      {
         readonly string? _resolved;
         public and_resolving_by_id() => _resolved = _index.TryResolve(_id);

         [XF] public void it_returns_the_full_path() => _resolved.Must().NotBeNull();
         [XF] public void the_path_points_to_an_existing_file() => File.Exists(_resolved!).Must().BeTrue();
      }

      public class and_getting_file_info : over_a_directory_with_guid_named_files
      {
         readonly MediaFileInfo? _info;
         public and_getting_file_info() => _info = _index.TryGetInfo(_id);

         [XF] public void it_returns_info() => _info.Must().NotBeNull();
         [XF] public void the_original_filename_comes_from_parent_directory() => _info!.OriginalFileName.Must().Be("natsume_ep01_03m22s.mp3");
         [XF] public void the_extension_is_extracted() => _info!.Extension.Must().Be(".mp3");
      }
   }

   public class over_a_directory_with_only_non_guid_files : When_building_a_MediaFileIndex
   {
      public over_a_directory_with_only_non_guid_files()
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
      public over_a_nonexistent_directory()
      {
         var index = new MediaFileIndex(Path.Combine(_tempDir, "does_not_exist"));
         index.Build();
      }

      [XF] public void it_handles_gracefully() => _index.Count.Must().Be(0);
   }

   public class without_explicit_Build_call : When_building_a_MediaFileIndex
   {
      readonly MediaFileId _id = MediaFileId.New();

      public without_explicit_Build_call()
      {
         var fileDir = Path.Combine(_tempDir, "test.mp3");
         Directory.CreateDirectory(fileDir);
         File.WriteAllText(Path.Combine(fileDir, $"{_id}.mp3"), "fake");
      }

      [XF] public void it_lazy_initializes_on_first_access() => _index.Contains(_id).Must().BeTrue();
   }

   public class resolving_an_unknown_id : When_building_a_MediaFileIndex
   {
      public resolving_an_unknown_id() => _index.Build();

      [XF] public void it_returns_null() => _index.TryResolve(MediaFileId.New()).Must().BeNull();
   }
}

public class When_configuring_media_routing
{
   public class with_multiple_rules : When_configuring_media_routing
   {
      readonly MediaRoutingConfig _config = new(
         [
            new MediaRoutingRule("anime::natsume", "commercial-001"),
            new MediaRoutingRule("anime", "commercial-002")
         ],
         "general");

      [XF] public void it_resolves_the_longest_matching_prefix() => _config.ResolveDirectory("anime::natsume::s1::01").Must().Be("commercial-001");
      [XF] public void it_falls_back_to_shorter_prefix() => _config.ResolveDirectory("anime::mushishi::s1::05").Must().Be("commercial-002");
   }

   public class with_no_matching_rule : When_configuring_media_routing
   {
      readonly MediaRoutingConfig _config = new(
         [new MediaRoutingRule("anime", "commercial-001")],
         "general");

      [XF] public void it_falls_back_to_default() => _config.ResolveDirectory("forvo").Must().Be("general");
   }

   public class with_default_config : When_configuring_media_routing
   {
      readonly MediaRoutingConfig _config = MediaRoutingConfig.Default();

      [XF] public void it_routes_everything_to_general() => _config.ResolveDirectory("anything").Must().Be("general");
   }
}

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

