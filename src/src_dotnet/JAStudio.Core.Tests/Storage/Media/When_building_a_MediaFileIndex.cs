using System;
using System.IO;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Storage.Media;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.Storage.Media;

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

   public class over_a_directory_with_a_guid_named_file : When_building_a_MediaFileIndex
   {
      readonly MediaFileId _id = MediaFileId.New();

      public over_a_directory_with_a_guid_named_file()
      {
         var fileDir = Path.Combine(_tempDir, "anime", "natsume", "natsume_ep01_03m22s.mp3");
         Directory.CreateDirectory(fileDir);
         File.WriteAllText(Path.Combine(fileDir, $"{_id}.mp3"), "fake audio");
         _index.Build();
      }

      [XF] public void it_indexes_the_file() => _index.Count.Must().Be(1);
      [XF] public void it_contains_the_id() => _index.Contains(_id).Must().BeTrue();

      public class and_resolving_by_id : over_a_directory_with_a_guid_named_file
      {
         readonly string? _resolved;
         public and_resolving_by_id() => _resolved = _index.TryResolve(_id);

         [XF] public void it_returns_the_full_path() => _resolved.Must().NotBeNull();
         [XF] public void the_path_points_to_an_existing_file() => File.Exists(_resolved!).Must().BeTrue();
      }

      public class and_getting_file_info : over_a_directory_with_a_guid_named_file
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
      readonly MediaFileIndex _nonexistentIndex;

      public over_a_nonexistent_directory()
      {
         _nonexistentIndex = new MediaFileIndex(Path.Combine(_tempDir, "does_not_exist"));
         _nonexistentIndex.Build();
      }

      [XF] public void it_indexes_nothing() => _nonexistentIndex.Count.Must().Be(0);
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
