using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
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

      foreach(var sidecarPath in Directory.EnumerateFiles(_mediaRoot, "*.audio.json", SearchOption.AllDirectories))
      {
         IndexSidecar(sidecarPath, isAudio: true);
      }

      foreach(var sidecarPath in Directory.EnumerateFiles(_mediaRoot, "*.image.json", SearchOption.AllDirectories))
      {
         IndexSidecar(sidecarPath, isAudio: false);
      }

      _initialized = true;
      this.Log().Info($"Media file index built: {_byId.Count} files indexed under {_mediaRoot}");
   }

   void IndexSidecar(string sidecarPath, bool isAudio)
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
      var mediaFileName = FindMediaFile(dir, attachment.Id);
      attachment.FilePath = mediaFileName ?? string.Empty;

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

   static string? FindMediaFile(string directory, MediaFileId id)
   {
      var idStr = id.ToString();
      foreach(var file in Directory.EnumerateFiles(directory, $"{idStr}.*"))
      {
         if(!file.EndsWith(".json", StringComparison.OrdinalIgnoreCase))
            return file;
      }

      return null;
   }

   void EnsureInitialized()
   {
      if(!_initialized) Build();
   }

   public string? TryResolve(MediaFileId id)
   {
      EnsureInitialized();
      return _byId.TryGetValue(id, out var attachment) ? attachment.FilePath : null;
   }

   public MediaAttachment? TryGetAttachment(MediaFileId id)
   {
      EnsureInitialized();
      return _byId.TryGetValue(id, out var attachment) ? attachment : null;
   }

   public MediaFileInfo? TryGetInfo(MediaFileId id)
   {
      EnsureInitialized();
      if(!_byId.TryGetValue(id, out var attachment)) return null;
      return new MediaFileInfo(attachment.Id, attachment.FilePath, attachment.OriginalFileName ?? string.Empty, Path.GetExtension(attachment.FilePath));
   }

   public NoteMedia GetNoteMedia(NoteId noteId)
   {
      EnsureInitialized();
      if(!_byNoteId.TryGetValue(noteId, out var attachments))
         return new NoteMedia([], []);

      var audio = attachments.OfType<AudioAttachment>().ToList();
      var images = attachments.OfType<ImageAttachment>().ToList();
      return new NoteMedia(audio, images);
   }

   public bool Contains(MediaFileId id)
   {
      EnsureInitialized();
      return _byId.ContainsKey(id);
   }

   public int Count
   {
      get
      {
         EnsureInitialized();
         return _byId.Count;
      }
   }

   public IReadOnlyCollection<MediaAttachment> All
   {
      get
      {
         EnsureInitialized();
         return _byId.Values;
      }
   }

   public bool ContainsByOriginalFileName(string originalFileName)
   {
      EnsureInitialized();
      return _byOriginalFileName.ContainsKey(originalFileName);
   }

   public MediaAttachment? TryGetByOriginalFileName(string originalFileName)
   {
      EnsureInitialized();
      return _byOriginalFileName.TryGetValue(originalFileName, out var attachment) ? attachment : null;
   }

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

