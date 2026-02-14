using System.IO;
using Compze.Utilities.Logging;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Storage.Media;

public class MediaSyncService : IMediaSyncService
{
   readonly string _ankiMediaDir;
   readonly string _audioDir;
   readonly string _imagesDir;

   public MediaSyncService(string ankiMediaDir, string databaseDir)
   {
      _ankiMediaDir = ankiMediaDir;
      _audioDir = Path.Combine(databaseDir, "files", "audio");
      _imagesDir = Path.Combine(databaseDir, "files", "images");
   }

   public void SyncMedia(JPNote note)
   {
      var references = note.GetMediaReferences();

      foreach (var reference in references)
      {
         var sourcePath = Path.Combine(_ankiMediaDir, reference.FileName);
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
