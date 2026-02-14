using System;
using System.IO;
using Compze.Utilities.Logging;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Storage.Media;

public class MediaSyncService : IMediaSyncService
{
   readonly Func<string> _ankiMediaDir;
   readonly string _audioDir;
   readonly string _imagesDir;

   public MediaSyncService(Func<string> ankiMediaDir, string databaseDir)
   {
      _ankiMediaDir = ankiMediaDir;
      _audioDir = Path.Combine(databaseDir, "files", "audio");
      _imagesDir = Path.Combine(databaseDir, "files", "images");
   }

   public void SyncMedia(JPNote note)
   {
      var references = note.GetMediaReferences();
      if (references.Count == 0) return;

      var ankiMediaDir = _ankiMediaDir();

      foreach (var reference in references)
      {
         var sourcePath = Path.Combine(ankiMediaDir, reference.FileName);
         var destDir = reference.Type == MediaType.Audio ? _audioDir : _imagesDir;
         var destPath = Path.Combine(destDir, reference.FileName);

         if (!File.Exists(sourcePath))
         {
            this.Log().Warning($"Media file not found in Anki media: {sourcePath}");
            continue;
         }

         if (File.Exists(destPath) && File.GetLastWriteTimeUtc(sourcePath) <= File.GetLastWriteTimeUtc(destPath))
            continue;

         Directory.CreateDirectory(destDir);
         File.Copy(sourcePath, destPath, overwrite: true);
      }
   }
}
