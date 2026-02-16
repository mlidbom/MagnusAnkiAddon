using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Compze.Utilities.Functional;
using Compze.Utilities.Logging;
using JAStudio.Core.Note;

namespace JAStudio.Core.Storage.Media;

public record MediaFileInfo(MediaFileId Id, string FullPath, string OriginalFileName, string Extension);

public class MediaFileIndex
{
   readonly Dictionary<MediaFileId, MediaAttachment> _byId = new();
   readonly Dictionary<string, MediaAttachment> _byOriginalFileName = new(StringComparer.OrdinalIgnoreCase);
   readonly Dictionary<NoteId, List<MediaAttachment>> _byNoteId = new();
   readonly string _mediaRoot;
   bool _initialized;

   public MediaFileIndex(string mediaRoot) => _mediaRoot = mediaRoot;

   public void Build()
   {
      _byId.Clear();
      _byOriginalFileName.Clear();
      _byNoteId.Clear();

      if(!Directory.Exists(_mediaRoot))
      {
         _initialized = true;
         return;
      }

      var audioSidecars = new List<string>();
      var imageSidecars = new List<string>();
      var mediaFilesByDirectory = new Dictionary<string, List<FileInfo>>(StringComparer.OrdinalIgnoreCase);

      foreach(var fi in new DirectoryInfo(_mediaRoot).EnumerateFiles("*", SearchOption.AllDirectories))
      {
         var fullName = fi.FullName;
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

      foreach(var sidecarPath in audioSidecars)
      {
         IndexSidecar(sidecarPath, isAudio: true, mediaFilesByDirectory);
      }

      foreach(var sidecarPath in imageSidecars)
      {
         IndexSidecar(sidecarPath, isAudio: false, mediaFilesByDirectory);
      }

      _initialized = true;
      this.Log().Info($"Media file index built: {_byId.Count} files indexed under {_mediaRoot}");
   }

   void IndexSidecar(string sidecarPath, bool isAudio, Dictionary<string, List<FileInfo>> mediaFilesByDirectory)
   {
      MediaAttachment attachment;
      try
      {
         attachment = isAudio
                         ? SidecarSerializer.ReadAudioSidecar(sidecarPath)
                         : SidecarSerializer.ReadImageSidecar(sidecarPath);
      }
      catch(Exception ex)
      {
         this.Log().Warning($"Failed to read sidecar {sidecarPath}: {ex.Message}");
         return;
      }

      var dir = Path.GetDirectoryName(sidecarPath) ?? string.Empty;
      attachment.FilePath = FindMediaFile(dir, attachment.Id, mediaFilesByDirectory) ?? string.Empty;

      if(!_byId.TryAdd(attachment.Id, attachment))
      {
         this.Log().Warning($"Duplicate media file ID {attachment.Id} in sidecar {sidecarPath}");
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
                    : new NoteMedia([], []));

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

   internal void Register(MediaAttachment attachment)
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
