using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace JAStudio.Core.Note.NoteFields;

public enum MediaType
{
   Audio,
   Image
}

public class MediaReference(string fileName, MediaType type)
{
   public string FileName { get; } = fileName;
   public MediaType Type { get; } = type;
}

public static partial class MediaFieldParsing
{
   public static List<MediaReference> ParseAudioReferences(string rawValue)
   {
      var results = new List<MediaReference>();
      if(string.IsNullOrWhiteSpace(rawValue)) return results;

      foreach(Match match in SoundTagRegex().Matches(rawValue))
      {
         var fileName = match.Groups[1].Value.Trim();
         if(!string.IsNullOrEmpty(fileName))
            results.Add(new MediaReference(fileName, MediaType.Audio));
      }

      return results;
   }

   public static List<MediaReference> ParseImageReferences(string rawValue)
   {
      var results = new List<MediaReference>();
      if(string.IsNullOrWhiteSpace(rawValue)) return results;

      foreach(Match match in ImgSrcRegex().Matches(rawValue))
      {
         var fileName = match.Groups[2].Value.Trim();
         if(!string.IsNullOrEmpty(fileName))
            results.Add(new MediaReference(fileName, MediaType.Image));
      }

      return results;
   }

   [GeneratedRegex(@"\[sound:([^\]]+)\]")]
   private static partial Regex SoundTagRegex();

   [GeneratedRegex(@"<img[^>]+src\s*=\s*([""'])(.*?)\1", RegexOptions.IgnoreCase)]
   private static partial Regex ImgSrcRegex();
}
