using System.Collections.Generic;
using System.IO;
using Compze.Utilities.Logging;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.Storage.Media;

public class MediaImportExecutor
{
   readonly string _ankiMediaDir;
   readonly MediaStorageService _storageService;
   readonly MediaFileIndex _index;

   public MediaImportExecutor(string ankiMediaDir, MediaStorageService storageService, MediaFileIndex index)
   {
      _ankiMediaDir = ankiMediaDir;
      _storageService = storageService;
      _index = index;
   }

   public void ImportVocabMedia(IReadOnlyList<VocabNote> notes, IReadOnlyList<VocabImportRule> rules)
   {
      var ruleSet = new MediaImportRuleSet(new List<VocabImportRule>(rules), [], []);

      foreach(var note in notes)
      {
         var sourceTag = ResolveSourceTag(note);
         var noteId = note.GetId();

         ImportField(note.Audio.First.GetMediaReferences(), ruleSet.TryResolveVocab(sourceTag, VocabMediaField.AudioFirst), sourceTag, noteId);
         ImportField(note.Audio.Second.GetMediaReferences(), ruleSet.TryResolveVocab(sourceTag, VocabMediaField.AudioSecond), sourceTag, noteId);
         ImportField(note.Audio.Tts.GetMediaReferences(), ruleSet.TryResolveVocab(sourceTag, VocabMediaField.AudioTts), sourceTag, noteId);
         ImportField(note.Image.GetMediaReferences(), ruleSet.TryResolveVocab(sourceTag, VocabMediaField.Image), sourceTag, noteId);
         ImportField(note.UserImage.GetMediaReferences(), ruleSet.TryResolveVocab(sourceTag, VocabMediaField.UserImage), sourceTag, noteId);
      }
   }

   public void ImportSentenceMedia(IReadOnlyList<SentenceNote> notes, IReadOnlyList<SentenceImportRule> rules)
   {
      var ruleSet = new MediaImportRuleSet([], new List<SentenceImportRule>(rules), []);

      foreach(var note in notes)
      {
         var sourceTag = ResolveSourceTag(note);
         var noteId = note.GetId();

         ImportField(note.Audio.GetMediaReferences(), ruleSet.TryResolveSentence(sourceTag, SentenceMediaField.Audio), sourceTag, noteId);
         ImportField(note.Screenshot.GetMediaReferences(), ruleSet.TryResolveSentence(sourceTag, SentenceMediaField.Screenshot), sourceTag, noteId);
      }
   }

   public void ImportKanjiMedia(IReadOnlyList<KanjiNote> notes, IReadOnlyList<KanjiImportRule> rules)
   {
      var ruleSet = new MediaImportRuleSet([], [], new List<KanjiImportRule>(rules));

      foreach(var note in notes)
      {
         var sourceTag = ResolveSourceTag(note);
         var noteId = note.GetId();

         ImportField(note.Audio.GetMediaReferences(), ruleSet.TryResolveKanji(sourceTag, KanjiMediaField.Audio), sourceTag, noteId);
         ImportField(note.Image.GetMediaReferences(), ruleSet.TryResolveKanji(sourceTag, KanjiMediaField.Image), sourceTag, noteId);
      }
   }

   void ImportField(List<MediaReference> references, VocabImportRule? rule, SourceTag sourceTag, NoteId noteId) =>
      ImportField(references, rule?.TargetDirectory, rule?.Copyright, sourceTag, noteId);

   void ImportField(List<MediaReference> references, SentenceImportRule? rule, SourceTag sourceTag, NoteId noteId) =>
      ImportField(references, rule?.TargetDirectory, rule?.Copyright, sourceTag, noteId);

   void ImportField(List<MediaReference> references, KanjiImportRule? rule, SourceTag sourceTag, NoteId noteId) =>
      ImportField(references, rule?.TargetDirectory, rule?.Copyright, sourceTag, noteId);

   void ImportField(List<MediaReference> references, string? targetDirectory, CopyrightStatus? copyright, SourceTag sourceTag, NoteId noteId)
   {
      if(targetDirectory == null || copyright == null) return;
      if(references.Count == 0) return;

      foreach(var reference in references)
      {
         var existing = _index.TryGetByOriginalFileName(reference.FileName);
         if(existing != null)
         {
            _storageService.AddNoteIdToExisting(existing, noteId);
            continue;
         }

         var sourcePath = Path.Combine(_ankiMediaDir, reference.FileName);
         if(!File.Exists(sourcePath))
         {
            this.Log().Warning($"Media file not found in Anki media: {sourcePath}");
            continue;
         }

         _storageService.StoreFile(sourcePath, targetDirectory, sourceTag, reference.FileName, noteId, reference.Type, copyright.Value);
      }
   }

   static readonly SourceTag FallbackSourceTag = SourceTag.Parse("anki::unknown");

   static SourceTag ResolveSourceTag(JPNote note)
   {
      var rawSourceTag = note.GetSourceTag();
      return string.IsNullOrEmpty(rawSourceTag) ? FallbackSourceTag : SourceTag.Parse($"{Tags.Source.Folder}{rawSourceTag}");
   }
}
