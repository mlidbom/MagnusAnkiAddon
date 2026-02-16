using System;
using System.Collections.Generic;
using System.IO;
using Compze.Utilities.Logging;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.Storage.Media;

public class AnkiMediaSyncService : IMediaSyncService
{
   static readonly SourceTag FallbackSourceTag = SourceTag.Parse("anki::unknown");

   readonly Func<string> _ankiMediaDir;
   readonly MediaStorageService _storageService;
   readonly MediaFileIndex _index;
   readonly MediaImportRoutingConfig<VocabMediaImportRule> _vocabRouting;
   readonly MediaImportRoutingConfig<SentenceMediaImportRule> _sentenceRouting;
   readonly MediaImportRoutingConfig<KanjiMediaImportRule> _kanjiRouting;

   public AnkiMediaSyncService(
      Func<string> ankiMediaDir,
      MediaStorageService storageService,
      MediaFileIndex index,
      MediaImportRoutingConfig<VocabMediaImportRule> vocabRouting,
      MediaImportRoutingConfig<SentenceMediaImportRule> sentenceRouting,
      MediaImportRoutingConfig<KanjiMediaImportRule> kanjiRouting)
   {
      _ankiMediaDir = ankiMediaDir;
      _storageService = storageService;
      _index = index;
      _vocabRouting = vocabRouting;
      _sentenceRouting = sentenceRouting;
      _kanjiRouting = kanjiRouting;
   }

   public void SyncMedia(JPNote note)
   {
      switch(note)
      {
         case VocabNote vocab:
            SyncVocabMedia(vocab);
            break;
         case SentenceNote sentence:
            SyncSentenceMedia(sentence);
            break;
         case KanjiNote kanji:
            SyncKanjiMedia(kanji);
            break;
      }
   }

   void SyncVocabMedia(VocabNote note)
   {
      var sourceTag = ResolveSourceTag(note);
      var rule = _vocabRouting.Resolve(sourceTag);
      var noteId = note.GetId();

      SyncField(note.Audio.First.GetMediaReferences(), rule.AudioFirst, sourceTag, noteId);
      SyncField(note.Audio.Second.GetMediaReferences(), rule.AudioSecond, sourceTag, noteId);
      SyncField(note.Audio.Tts.GetMediaReferences(), rule.AudioTts, sourceTag, noteId);
      SyncField(note.Image.GetMediaReferences(), rule.Image, sourceTag, noteId);
      SyncField(note.UserImage.GetMediaReferences(), rule.UserImage, sourceTag, noteId);
   }

   void SyncSentenceMedia(SentenceNote note)
   {
      var sourceTag = ResolveSourceTag(note);
      var rule = _sentenceRouting.Resolve(sourceTag);
      var noteId = note.GetId();

      SyncField(note.Audio.GetMediaReferences(), rule.Audio, sourceTag, noteId);
      SyncField(note.Screenshot.GetMediaReferences(), rule.Screenshot, sourceTag, noteId);
   }

   void SyncKanjiMedia(KanjiNote note)
   {
      var sourceTag = ResolveSourceTag(note);
      var rule = _kanjiRouting.Resolve(sourceTag);
      var noteId = note.GetId();

      SyncField(note.Audio.GetMediaReferences(), rule.Audio, sourceTag, noteId);
      SyncField(note.Image.GetMediaReferences(), rule.Image, sourceTag, noteId);
   }

   void SyncField(List<MediaReference> references, MediaImportRoute route, SourceTag sourceTag, NoteId noteId)
   {
      if(references.Count == 0) return;

      var ankiMediaDir = _ankiMediaDir();

      foreach(var reference in references)
      {
         var existing = _index.TryGetByOriginalFileName(reference.FileName);
         if(existing != null)
         {
            _storageService.AddNoteIdToExisting(existing, noteId);
            continue;
         }

         var sourcePath = Path.Combine(ankiMediaDir, reference.FileName);
         if(!File.Exists(sourcePath))
         {
            this.Log().Warning($"Media file not found in Anki media: {sourcePath}");
            continue;
         }

         _storageService.StoreFile(sourcePath, route.TargetDirectory, sourceTag, reference.FileName, noteId, reference.Type, route.Copyright);
      }
   }

   static SourceTag ResolveSourceTag(JPNote note)
   {
      var rawSourceTag = note.GetSourceTag();
      return string.IsNullOrEmpty(rawSourceTag) ? FallbackSourceTag : SourceTag.Parse($"{Tags.Source.Folder}{rawSourceTag}");
   }
}

