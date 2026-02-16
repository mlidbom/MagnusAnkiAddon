using System;
using System.IO;
using Compze.Utilities.Logging;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Storage.Media;

public class AnkiMediaSyncService : IMediaSyncService
{
   static readonly SourceTag FallbackSourceTag = SourceTag.Parse("anki::unknown");

   readonly Func<string> _ankiMediaDir;
   readonly MediaStorageService _storageService;
   readonly MediaFileIndex _index;

   public AnkiMediaSyncService(Func<string> ankiMediaDir, MediaStorageService storageService, MediaFileIndex index)
   {
      _ankiMediaDir = ankiMediaDir;
      _storageService = storageService;
      _index = index;
   }

   public void SyncMedia(JPNote note)
   {
      var references = note.MediaReferences;
      if(references.Count == 0) return;

      var ankiMediaDir = _ankiMediaDir();
      var noteId = note.GetId();
      var rawSourceTag = note.GetSourceTag();
      var sourceTag = string.IsNullOrEmpty(rawSourceTag) ? FallbackSourceTag : SourceTag.Parse($"{Tags.Source.Folder}{rawSourceTag}");

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

         var copyright = reference.Type == MediaType.Audio ? CopyrightStatus.Free : CopyrightStatus.Free;
         _storageService.StoreFile(sourcePath, sourceTag, reference.FileName, noteId, reference.Type, copyright);
      }
   }
}

