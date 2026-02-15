using System;
using System.Collections.Generic;
using System.IO;
using Compze.Utilities.Logging;

namespace JAStudio.Core.Storage.Media;

public record MediaFileInfo(MediaFileId Id, string FullPath, string OriginalFileName, string Extension);

public class MediaFileIndex
{
   readonly Dictionary<MediaFileId, MediaFileInfo> _index = new();
   readonly Dictionary<string, MediaFileInfo> _byOriginalFileName = new(StringComparer.OrdinalIgnoreCase);
   readonly string _mediaRoot;
   bool _initialized;

   public MediaFileIndex(string mediaRoot) => _mediaRoot = mediaRoot;

   public void Build()
   {
      _index.Clear();
      _byOriginalFileName.Clear();

      if(!Directory.Exists(_mediaRoot))
      {
         _initialized = true;
         return;
      }

      foreach(var file in Directory.EnumerateFiles(_mediaRoot, "*.*", SearchOption.AllDirectories))
      {
         var fileNameWithoutExtension = Path.GetFileNameWithoutExtension(file);
         if(!MediaFileId.TryParse(fileNameWithoutExtension, out var mediaFileId)) continue;

         var extension = Path.GetExtension(file);
         var originalFileName = Path.GetFileName(Path.GetDirectoryName(file)) ?? string.Empty;

         var info = new MediaFileInfo(mediaFileId, file, originalFileName, extension);

         if(!_index.TryAdd(mediaFileId, info))
         {
            this.Log().Warning($"Duplicate media file ID {mediaFileId} found at {file} — already indexed at {_index[mediaFileId].FullPath}");
         }

         _byOriginalFileName.TryAdd(info.OriginalFileName, info);
      }

      _initialized = true;
      this.Log().Info($"Media file index built: {_index.Count} files indexed under {_mediaRoot}");
   }

   void EnsureInitialized()
   {
      if(!_initialized) Build();
   }

   public string? TryResolve(MediaFileId id)
   {
      EnsureInitialized();
      return _index.TryGetValue(id, out var info) ? info.FullPath : null;
   }

   public MediaFileInfo? TryGetInfo(MediaFileId id)
   {
      EnsureInitialized();
      return _index.TryGetValue(id, out var info) ? info : null;
   }

   public bool Contains(MediaFileId id)
   {
      EnsureInitialized();
      return _index.ContainsKey(id);
   }

   public int Count
   {
      get
      {
         EnsureInitialized();
         return _index.Count;
      }
   }

   public IReadOnlyCollection<MediaFileInfo> All
   {
      get
      {
         EnsureInitialized();
         return _index.Values;
      }
   }

   public bool ContainsByOriginalFileName(string originalFileName)
   {
      EnsureInitialized();
      return _byOriginalFileName.ContainsKey(originalFileName);
   }

   internal void Register(MediaFileInfo info)
   {
      _index[info.Id] = info;
      _byOriginalFileName.TryAdd(info.OriginalFileName, info);
   }
}
