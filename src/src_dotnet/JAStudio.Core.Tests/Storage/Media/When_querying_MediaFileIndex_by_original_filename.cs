using System;
using System.IO;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Storage.Media;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.Storage.Media;

public class When_querying_MediaFileIndex_by_original_filename : IDisposable
{
   readonly string _tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");
   readonly MediaFileIndex _index;

   public When_querying_MediaFileIndex_by_original_filename()
   {
      Directory.CreateDirectory(_tempDir);
      _index = new MediaFileIndex(_tempDir);
   }

   public void Dispose() => Directory.Delete(_tempDir, recursive: true);

   public class with_an_indexed_file : When_querying_MediaFileIndex_by_original_filename
   {
      public with_an_indexed_file()
      {
         var id = MediaFileId.New();
         var fileDir = Path.Combine(_tempDir, "test_audio.mp3");
         Directory.CreateDirectory(fileDir);
         File.WriteAllText(Path.Combine(fileDir, $"{id}.mp3"), "fake");
         _index.Build();
      }

      [XF] public void it_finds_by_exact_name() =>
         _index.ContainsByOriginalFileName("test_audio.mp3").Must().BeTrue();

      [XF] public void it_finds_case_insensitively() =>
         _index.ContainsByOriginalFileName("TEST_AUDIO.MP3").Must().BeTrue();

      [XF] public void it_returns_false_for_unknown_name() =>
         _index.ContainsByOriginalFileName("nonexistent.mp3").Must().BeFalse();
   }

   public class with_a_registered_file : When_querying_MediaFileIndex_by_original_filename
   {
      public with_a_registered_file()
      {
         var id = MediaFileId.New();
         _index.Build();
         _index.Register(new MediaFileInfo(id, Path.Combine(_tempDir, $"{id}.mp3"), "registered.mp3", ".mp3"));
      }

      [XF] public void it_is_found_by_original_name() =>
         _index.ContainsByOriginalFileName("registered.mp3").Must().BeTrue();
   }
}
