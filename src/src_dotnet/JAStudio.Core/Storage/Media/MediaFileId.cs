using System;

namespace JAStudio.Core.Storage.Media;

public readonly struct MediaFileId(Guid value) : IEquatable<MediaFileId>
{
   public Guid Value { get; } = value;

   public static MediaFileId New() => new(Guid.NewGuid());

   public static MediaFileId Parse(string value) => new(Guid.Parse(value));

   public static bool TryParse(string? value, out MediaFileId result)
   {
      if(Guid.TryParse(value, out var guid))
      {
         result = new MediaFileId(guid);
         return true;
      }

      result = default;
      return false;
   }

   public bool IsEmpty => Value == Guid.Empty;

   public override string ToString() => Value.ToString("D");

   public bool Equals(MediaFileId other) => Value == other.Value;
   public override bool Equals(object? obj) => obj is MediaFileId other && Equals(other);
   public override int GetHashCode() => Value.GetHashCode();
   public static bool operator ==(MediaFileId left, MediaFileId right) => left.Equals(right);
   public static bool operator !=(MediaFileId left, MediaFileId right) => !left.Equals(right);
}
