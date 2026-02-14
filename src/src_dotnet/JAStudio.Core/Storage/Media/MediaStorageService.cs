using System.IO;

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

   public MediaFileId StoreFile(string sourceFilePath, string sourceTag, string originalFileName)
   {
      var id = MediaFileId.New();
      StoreFileWithId(id, sourceFilePath, sourceTag, originalFileName);
      return id;
   }

   public void StoreFileWithId(MediaFileId id, string sourceFilePath, string sourceTag, string originalFileName)
   {
      var destPath = BuildStoragePath(id, sourceTag, originalFileName);

      Directory.CreateDirectory(Path.GetDirectoryName(destPath)!);
      File.Copy(sourceFilePath, destPath, overwrite: false);

      var extension = Path.GetExtension(destPath);
      _index.Register(new MediaFileInfo(id, destPath, originalFileName, extension));
   }

   public string? TryResolve(MediaFileId id) => _index.TryResolve(id);

   public bool Exists(MediaFileId id) => _index.Contains(id);

   string BuildStoragePath(MediaFileId id, string sourceTag, string originalFileName)
   {
      var routedDirectory = _routingConfig.ResolveDirectory(sourceTag);
      var tagPath = sourceTag.Replace("::", Path.DirectorySeparatorChar.ToString());
      var extension = Path.GetExtension(originalFileName);

      // {mediaRoot}/{routedDirectory}/{source/tag/path}/{originalFileName}/{id}.{ext}
      return Path.Combine(_mediaRoot, routedDirectory, tagPath, originalFileName, $"{id}{extension}");
   }
}
