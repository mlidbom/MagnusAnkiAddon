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
   readonly MediaImportRuleSet _ruleSet;

   public AnkiMediaSyncService(
      Func<string> ankiMediaDir,
      MediaStorageService storageService,
      MediaFileIndex index,
      MediaImportRuleSet ruleSet)
   {
      _ankiMediaDir = ankiMediaDir;
      _storageService = storageService;
      _index = index;
      _ruleSet = ruleSet;
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
      var noteId = note.GetId();

      SyncField(note.Audio.First.GetMediaReferences(), _ruleSet.TryResolveVocab(sourceTag, VocabMediaField.AudioFirst), sourceTag, noteId);
      SyncField(note.Audio.Second.GetMediaReferences(), _ruleSet.TryResolveVocab(sourceTag, VocabMediaField.AudioSecond), sourceTag, noteId);
      SyncField(note.Audio.Tts.GetMediaReferences(), _ruleSet.TryResolveVocab(sourceTag, VocabMediaField.AudioTts), sourceTag, noteId);
      SyncField(note.Image.GetMediaReferences(), _ruleSet.TryResolveVocab(sourceTag, VocabMediaField.Image), sourceTag, noteId);
      SyncField(note.UserImage.GetMediaReferences(), _ruleSet.TryResolveVocab(sourceTag, VocabMediaField.UserImage), sourceTag, noteId);
   }

   void SyncSentenceMedia(SentenceNote note)
   {
      var sourceTag = ResolveSourceTag(note);
      var noteId = note.GetId();

      SyncField(note.Audio.GetMediaReferences(), _ruleSet.TryResolveSentence(sourceTag, SentenceMediaField.Audio), sourceTag, noteId);
      SyncField(note.Screenshot.GetMediaReferences(), _ruleSet.TryResolveSentence(sourceTag, SentenceMediaField.Screenshot), sourceTag, noteId);
   }

   void SyncKanjiMedia(KanjiNote note)
   {
      var sourceTag = ResolveSourceTag(note);
      var noteId = note.GetId();

      SyncField(note.Audio.GetMediaReferences(), _ruleSet.TryResolveKanji(sourceTag, KanjiMediaField.Audio), sourceTag, noteId);
      SyncField(note.Image.GetMediaReferences(), _ruleSet.TryResolveKanji(sourceTag, KanjiMediaField.Image), sourceTag, noteId);
   }

   void SyncField(List<MediaReference> references, VocabImportRule? rule, SourceTag sourceTag, NoteId noteId) =>
      SyncField(references, rule?.TargetDirectory, rule?.Copyright, sourceTag, noteId);

   void SyncField(List<MediaReference> references, SentenceImportRule? rule, SourceTag sourceTag, NoteId noteId) =>
      SyncField(references, rule?.TargetDirectory, rule?.Copyright, sourceTag, noteId);

   void SyncField(List<MediaReference> references, KanjiImportRule? rule, SourceTag sourceTag, NoteId noteId) =>
      SyncField(references, rule?.TargetDirectory, rule?.Copyright, sourceTag, noteId);

   void SyncField(List<MediaReference> references, string? targetDirectory, CopyrightStatus? copyright, SourceTag sourceTag, NoteId noteId)
   {
      if(targetDirectory == null || copyright == null) return;
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

         _storageService.StoreFile(sourcePath, targetDirectory, sourceTag, reference.FileName, noteId, reference.Type, copyright.Value);
      }
   }

   static SourceTag ResolveSourceTag(JPNote note)
   {
      var rawSourceTag = note.GetSourceTag();
      return string.IsNullOrEmpty(rawSourceTag) ? FallbackSourceTag : SourceTag.Parse($"{Tags.Source.Folder}{rawSourceTag}");
   }
}

