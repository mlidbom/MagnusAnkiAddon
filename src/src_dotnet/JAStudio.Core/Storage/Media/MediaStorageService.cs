using System.Collections.Generic;
using System.IO;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Storage.Media;

public class MediaStorageService
{
   readonly string _mediaRoot;
   readonly MediaFileIndex _index;
   readonly MediaRoutingConfig _routingConfig;

   public MediaStorageService(string mediaRoot, MediaFileIndex index, MediaRoutingConfig routingConfig)
   {
      _mediaRoot = mediaRoot;
      _index = index;
      _routingConfig = routingConfig;
   }

   public MediaFileId StoreFile(string sourceFilePath, string sourceTag, string originalFileName, NoteId noteId, string? ankiFieldName, MediaType mediaType, CopyrightStatus copyright, TtsInfo? tts = null)
   {
      var id = MediaFileId.New();
      var destPath = BuildStoragePath(id, sourceTag, originalFileName);

      Directory.CreateDirectory(Path.GetDirectoryName(destPath)!);
      File.Copy(sourceFilePath, destPath, overwrite: false);

      MediaAttachment attachment;
      if(mediaType == MediaType.Audio)
      {
         var audio = new AudioAttachment
                     {
                        Id = id,
                        NoteIds = [noteId],
                        NoteSourceTag = sourceTag,
                        AnkiFieldName = ankiFieldName,
                        OriginalFileName = originalFileName,
                        Copyright = copyright,
                        Tts = tts
                     };

         audio.FilePath = destPath;
         var sidecarPath = SidecarSerializer.BuildAudioSidecarPath(destPath);
         SidecarSerializer.WriteAudioSidecar(sidecarPath, audio);
         attachment = audio;
      }
      else
      {
         var image = new ImageAttachment
                     {
                        Id = id,
                        NoteIds = [noteId],
                        NoteSourceTag = sourceTag,
                        AnkiFieldName = ankiFieldName,
                        OriginalFileName = originalFileName,
                        Copyright = copyright
                     };

         image.FilePath = destPath;
         var sidecarPath = SidecarSerializer.BuildImageSidecarPath(destPath);
         SidecarSerializer.WriteImageSidecar(sidecarPath, image);
         attachment = image;
      }

      _index.Register(attachment);
      return id;
   }

   public void AddNoteIdToExisting(MediaAttachment existing, NoteId noteId)
   {
      if(existing.NoteIds.Contains(noteId)) return;
      existing.NoteIds.Add(noteId);

      if(string.IsNullOrEmpty(existing.FilePath)) return;

      if(existing is AudioAttachment audio)
      {
         var sidecarPath = SidecarSerializer.BuildAudioSidecarPath(existing.FilePath);
         SidecarSerializer.WriteAudioSidecar(sidecarPath, audio);
      }
      else if(existing is ImageAttachment image)
      {
         var sidecarPath = SidecarSerializer.BuildImageSidecarPath(existing.FilePath);
         SidecarSerializer.WriteImageSidecar(sidecarPath, image);
      }
   }

   public string? TryResolve(MediaFileId id) => _index.TryResolve(id);

   public bool Exists(MediaFileId id) => _index.Contains(id);

   string BuildStoragePath(MediaFileId id, string sourceTag, string originalFileName)
   {
      var routedDirectory = _routingConfig.ResolveDirectory(sourceTag);
      var bucket = id.ToString()[..2];
      var extension = Path.GetExtension(originalFileName);

      // {mediaRoot}/{routedDirectory}/{bucket}/{id}.{ext}
      return Path.Combine(_mediaRoot, routedDirectory, bucket, $"{id}{extension}");
   }
}

