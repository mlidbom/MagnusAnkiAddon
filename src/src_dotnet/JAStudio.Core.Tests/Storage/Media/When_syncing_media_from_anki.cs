using System;
using System.IO;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Storage.Media;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.Storage.Media;

public class When_syncing_media_from_anki : TestStartingWithEmptyCollection, IDisposable
{
   readonly string _tempDir = Path.Combine(Path.GetTempPath(), $"JAStudio_test_{Guid.NewGuid():N}");
   readonly string _ankiMediaDir;
   readonly string _mediaRoot;
   readonly MediaFileIndex _index;
   readonly MediaStorageService _storageService;
   readonly AnkiMediaSyncService _syncService;

   public When_syncing_media_from_anki()
   {
      _ankiMediaDir = Path.Combine(_tempDir, "anki_media");
      _mediaRoot = Path.Combine(_tempDir, "corpus_files");
      Directory.CreateDirectory(_ankiMediaDir);
      Directory.CreateDirectory(_mediaRoot);

      _index = new MediaFileIndex(_mediaRoot);
      var config = MediaRoutingConfig.Default();
      _storageService = new MediaStorageService(_mediaRoot, _index, config);
      _syncService = new AnkiMediaSyncService(() => _ankiMediaDir, _storageService, _index);
   }

   public new void Dispose()
   {
      base.Dispose();
      Directory.Delete(_tempDir, recursive: true);
   }

   void CreateAnkiMediaFile(string fileName, string content = "fake content")
   {
      File.WriteAllText(Path.Combine(_ankiMediaDir, fileName), content);
   }

   public class for_a_vocab_note_with_audio_and_image : When_syncing_media_from_anki
   {
      public for_a_vocab_note_with_audio_and_image()
      {
         CreateAnkiMediaFile("vocab_audio.mp3");
         CreateAnkiMediaFile("vocab_image.jpg");

         var note = CreateVocab("走る", "to run", "はしる");
         note.Audio.First.SetRawValue("[sound:vocab_audio.mp3]");
         note.Image.SetRawValue("<img src=\"vocab_image.jpg\">");

         _syncService.SyncMedia(note);
      }

      [XF] public void it_copies_the_audio_file() => _index.Count.Must().Be(2);

      [XF] public void the_audio_file_is_indexed_by_original_name() =>
         _index.ContainsByOriginalFileName("vocab_audio.mp3").Must().BeTrue();

      [XF] public void the_image_file_is_indexed_by_original_name() =>
         _index.ContainsByOriginalFileName("vocab_image.jpg").Must().BeTrue();
   }

   public class for_a_kanji_note_with_audio : When_syncing_media_from_anki
   {
      public for_a_kanji_note_with_audio()
      {
         CreateAnkiMediaFile("kanji_audio.mp3");

         var note = CreateKanji("本", "book", "ホン", "もと");
         note.Audio.SetRawValue("[sound:kanji_audio.mp3]");

         _syncService.SyncMedia(note);
      }

      [XF] public void it_copies_the_audio_file() => _index.Count.Must().Be(1);

      [XF] public void the_file_is_indexed_by_original_name() =>
         _index.ContainsByOriginalFileName("kanji_audio.mp3").Must().BeTrue();
   }

   public class for_a_sentence_note_with_audio_and_screenshot : When_syncing_media_from_anki
   {
      public for_a_sentence_note_with_audio_and_screenshot()
      {
         CreateAnkiMediaFile("sentence_audio.mp3");
         CreateAnkiMediaFile("screenshot.png");

         var note = CreateSentence("テスト文");
         note.Audio.SetRawValue("[sound:sentence_audio.mp3]");
         note.Screenshot.SetRawValue("<img src=\"screenshot.png\">");

         _syncService.SyncMedia(note);
      }

      [XF] public void it_copies_both_files() => _index.Count.Must().Be(2);

      [XF] public void the_audio_is_indexed() =>
         _index.ContainsByOriginalFileName("sentence_audio.mp3").Must().BeTrue();

      [XF] public void the_screenshot_is_indexed() =>
         _index.ContainsByOriginalFileName("screenshot.png").Must().BeTrue();
   }

   public class when_a_file_is_already_stored : When_syncing_media_from_anki
   {
      readonly int _countAfterSecondSync;

      public when_a_file_is_already_stored()
      {
         CreateAnkiMediaFile("already_stored.mp3");

         var note = CreateVocab("食べる", "to eat", "たべる");
         note.Audio.First.SetRawValue("[sound:already_stored.mp3]");

         _syncService.SyncMedia(note);
         var countAfterFirstSync = _index.Count;
         countAfterFirstSync.Must().Be(1);

         _syncService.SyncMedia(note);
         _countAfterSecondSync = _index.Count;
      }

      [XF] public void it_does_not_duplicate_the_file() => _countAfterSecondSync.Must().Be(1);
   }

   public class when_the_source_file_is_missing : When_syncing_media_from_anki
   {
      public when_the_source_file_is_missing()
      {
         var note = CreateVocab("飲む", "to drink", "のむ");
         note.Audio.First.SetRawValue("[sound:missing_audio.mp3]");

         _syncService.SyncMedia(note);
      }

      [XF] public void it_skips_the_file_gracefully() => _index.Count.Must().Be(0);
   }

   public class when_the_note_has_no_media : When_syncing_media_from_anki
   {
      public when_the_note_has_no_media()
      {
         var note = CreateVocab("見る", "to see", "みる");
         _syncService.SyncMedia(note);
      }

      [XF] public void it_does_nothing() => _index.Count.Must().Be(0);
   }

   public class verifying_storage_path_routing : When_syncing_media_from_anki
   {
      readonly MediaFileInfo? _audioInfo;
      readonly MediaFileInfo? _imageInfo;

      public verifying_storage_path_routing()
      {
         CreateAnkiMediaFile("routed_audio.mp3");
         CreateAnkiMediaFile("routed_image.jpg");

         var note = CreateVocab("書く", "to write", "かく");
         note.Audio.First.SetRawValue("[sound:routed_audio.mp3]");
         note.Image.SetRawValue("<img src=\"routed_image.jpg\">");

         _syncService.SyncMedia(note);

         foreach(var info in _index.All)
         {
            if(info.OriginalFileName == "routed_audio.mp3") _audioInfo = info;
            if(info.OriginalFileName == "routed_image.jpg") _imageInfo = info;
         }
      }

      [XF] public void the_audio_is_stored_under_anki_audio_path() =>
         _audioInfo!.FullPath.Must().Contain(Path.Combine("anki", "audio"));

      [XF] public void the_image_is_stored_under_anki_image_path() =>
         _imageInfo!.FullPath.Must().Contain(Path.Combine("anki", "image"));
   }
}
