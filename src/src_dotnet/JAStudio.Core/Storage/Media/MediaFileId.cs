using System;

namespace JAStudio.Core.Storage.Media;

public readonly record struct MediaFileId(Guid Value)
{
   public static MediaFileId New() => new(Guid.NewGuid());

   public static MediaFileId Parse(string value) => new(Guid.Parse(value));

   public static bool TryParse(string? value, out MediaFileId result)
   {
      if (Guid.TryParse(value, out var guid))
      {
         result = new MediaFileId(guid);
         return true;
      }

      result = default;
      return false;
   }

   public bool IsEmpty => Value == Guid.Empty;

   public override string ToString() => Value.ToString("D");
}
