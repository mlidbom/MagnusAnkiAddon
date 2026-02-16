using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Compze.Utilities.Functional;
using Compze.Utilities.Logging;
using JAStudio.Core.Note;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Storage.Media;

public record MediaFileInfo(MediaFileId Id, string FullPath, string OriginalFileName, string Extension);

public class MediaFileIndex
{
   readonly Dictionary<MediaFileId, MediaAttachment> _byId = new();
   readonly Dictionary<string, MediaAttachment> _byOriginalFileName = new(StringComparer.OrdinalIgnoreCase);
   readonly Dictionary<NoteId, List<MediaAttachment>> _byNoteId = new();
   readonly string _mediaRoot;
   readonly TaskRunner _taskRunner;
   bool _initialized;

   public MediaFileIndex(string mediaRoot, TaskRunner taskRunner)
   {
      _mediaRoot = mediaRoot;
      _taskRunner = taskRunner;
   }

   record MediaScanResult(
      List<string> AudioSidecarPaths,
      List<string> ImageSidecarPaths,
      Dictionary<string, List<FileInfo>> MediaFilesByDirectory);

   /// <summary>
   /// Builds the index with progress reporting via RunBatch.
   /// Single filesystem enumeration, then parallel sidecar deserialization.
   /// </summary>
   public void Build()
   {
      ClearIndexes();

      if(!Directory.Exists(_mediaRoot))
      {
         _initialized = true;
         return;
      }

      using var scope = _taskRunner.Current("Loading media index");

      var scan = scope.RunIndeterminate("Scanning media files", ScanMediaFiles);

      var audioAttachments = scope.RunBatch(scan.AudioSidecarPaths, path => DeserializeSidecar(path, isAudio: true, scan.MediaFilesByDirectory), "Loading audio sidecars", ThreadCount.FractionOfLogicalCores(0.3));
      var imageAttachments = scope.RunBatch(scan.ImageSidecarPaths, path => DeserializeSidecar(path, isAudio: false, scan.MediaFilesByDirectory), "Loading image sidecars", ThreadCount.FractionOfLogicalCores(0.3));

      scope.RunIndeterminate("Building media indexes",
                             () =>
                             {
                                foreach(var attachment in audioAttachments) IndexAttachment(attachment);
                                foreach(var attachment in imageAttachments) IndexAttachment(attachment);
                             });

      _initialized = true;
      this.Log().Info($"Media file index built: {_byId.Count} files indexed under {_mediaRoot}");
   }

   void ClearIndexes()
   {
      _byId.Clear();
      _byOriginalFileName.Clear();
      _byNoteId.Clear();
   }

   /// <summary>
   /// Single enumeration of the media directory tree. Separates files into
   /// audio sidecar paths, image sidecar paths, and media files grouped by directory.
   /// </summary>
   MediaScanResult ScanMediaFiles()
   {
      var audioSidecars = new List<string>();
      var imageSidecars = new List<string>();
      var mediaFilesByDirectory = new Dictionary<string, List<FileInfo>>(StringComparer.OrdinalIgnoreCase);

      var metadataPrefix = App.MetadataDir + Path.DirectorySeparatorChar;

      foreach(var fi in new DirectoryInfo(_mediaRoot).EnumerateFiles("*", SearchOption.AllDirectories))
      {
         var fullName = fi.FullName;
         if(fullName.StartsWith(metadataPrefix, StringComparison.OrdinalIgnoreCase))
            continue;

         if(fullName.EndsWith(SidecarSerializer.AudioSidecarExtension, StringComparison.OrdinalIgnoreCase))
         {
            audioSidecars.Add(fullName);
         } else if(fullName.EndsWith(SidecarSerializer.ImageSidecarExtension, StringComparison.OrdinalIgnoreCase))
         {
            imageSidecars.Add(fullName);
         } else
         {
            var dir = fi.DirectoryName ?? string.Empty;
            if(!mediaFilesByDirectory.TryGetValue(dir, out var list))
            {
               list = [];
               mediaFilesByDirectory[dir] = list;
            }

            list.Add(fi);
         }
      }

      return new MediaScanResult(audioSidecars, imageSidecars, mediaFilesByDirectory);
   }

   static MediaAttachment DeserializeSidecar(string sidecarPath, bool isAudio, Dictionary<string, List<FileInfo>> mediaFilesByDirectory)
   {
      MediaAttachment attachment = isAudio
                                      ? SidecarSerializer.ReadAudioSidecar(sidecarPath)
                                      : SidecarSerializer.ReadImageSidecar(sidecarPath);

      var dir = Path.GetDirectoryName(sidecarPath) ?? string.Empty;
      attachment.FilePath = FindMediaFile(dir, attachment.Id, mediaFilesByDirectory) ?? string.Empty;
      return attachment;
   }

   void IndexAttachment(MediaAttachment attachment)
   {
      if(!_byId.TryAdd(attachment.Id, attachment))
      {
         this.Log().Warning($"Duplicate media file ID {attachment.Id}");
         return;
      }

      if(attachment.OriginalFileName != null)
      {
         _byOriginalFileName.TryAdd(attachment.OriginalFileName, attachment);
      }

      foreach(var noteId in attachment.NoteIds)
      {
         if(!_byNoteId.TryGetValue(noteId, out var list))
         {
            list = [];
            _byNoteId[noteId] = list;
         }

         list.Add(attachment);
      }
   }

   static string? FindMediaFile(string directory, MediaFileId id, Dictionary<string, List<FileInfo>> mediaFilesByDirectory)
   {
      if(!mediaFilesByDirectory.TryGetValue(directory, out var files)) return null;

      var idStr = id.ToString();
      foreach(var fi in files)
      {
         if(Path.GetFileNameWithoutExtension(fi.Name) == idStr)
            return fi.FullName;
      }

      return null;
   }

   unit EnsureInitialized() => unit.From(() =>
   {
      if(!_initialized) Build();
   });

   public string? TryResolve(MediaFileId id) => EnsureInitialized()
     .then(() => _byId.TryGetValue(id, out var attachment) ? attachment.FilePath : null);

   public MediaAttachment? TryGetAttachment(MediaFileId id) => EnsureInitialized()
     .then(() => _byId.TryGetValue(id, out var attachment) ? attachment : null);

   public MediaFileInfo? TryGetInfo(MediaFileId id) => EnsureInitialized()
     .then(() => _byId.TryGetValue(id, out var attachment)
                    ? new MediaFileInfo(attachment.Id, attachment.FilePath, attachment.OriginalFileName ?? string.Empty, Path.GetExtension(attachment.FilePath))
                    : null);

   public NoteMedia GetNoteMedia(NoteId noteId) => EnsureInitialized()
     .then(() => _byNoteId.TryGetValue(noteId, out var attachments)
                    ? new NoteMedia(attachments.OfType<AudioAttachment>().ToList(), attachments.OfType<ImageAttachment>().ToList())
                    : NoteMedia.Empty);

   public bool Contains(MediaFileId id) => EnsureInitialized()
     .then(() => _byId.ContainsKey(id));

   public int Count => EnsureInitialized()
     .then(() => _byId.Count);

   public IReadOnlyCollection<MediaAttachment> All => EnsureInitialized()
     .then(() => _byId.Values);

   public bool ContainsByOriginalFileName(string originalFileName) => EnsureInitialized()
     .then(() => _byOriginalFileName.ContainsKey(originalFileName));

   public MediaAttachment? TryGetByOriginalFileName(string originalFileName) => EnsureInitialized()
     .then(() => _byOriginalFileName.TryGetValue(originalFileName, out var attachment) ? attachment : null);

   public void Register(MediaAttachment attachment)
   {
      _byId[attachment.Id] = attachment;

      if(attachment.OriginalFileName != null)
      {
         _byOriginalFileName.TryAdd(attachment.OriginalFileName, attachment);
      }

      foreach(var noteId in attachment.NoteIds)
      {
         if(!_byNoteId.TryGetValue(noteId, out var list))
         {
            list = [];
            _byNoteId[noteId] = list;
         }

         list.Add(attachment);
      }
   }
}
