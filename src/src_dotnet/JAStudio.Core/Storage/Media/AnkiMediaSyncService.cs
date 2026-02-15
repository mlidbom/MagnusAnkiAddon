using System;
using System.IO;
using Compze.Utilities.Logging;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Storage.Media;

public class AnkiMediaSyncService : IMediaSyncService
{
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

      foreach(var reference in references)
      {
         if(_index.ContainsByOriginalFileName(reference.FileName)) continue;

         var sourcePath = Path.Combine(ankiMediaDir, reference.FileName);
         if(!File.Exists(sourcePath))
         {
            this.Log().Warning($"Media file not found in Anki media: {sourcePath}");
            continue;
         }

         var sourceTag = reference.Type == MediaType.Audio ? "anki::audio" : "anki::image";
         _storageService.StoreFile(sourcePath, sourceTag, reference.FileName);
      }
   }
}
