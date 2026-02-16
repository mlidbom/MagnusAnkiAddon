using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Storage.Media;

public sealed class SourceTag : IEquatable<SourceTag>
{
   const string Separator = "::";

   readonly string _value;
   readonly string[] _segments;

   SourceTag(string value, string[] segments)
   {
      _value = value;
      _segments = segments;
   }

   public static SourceTag Parse(string value)
   {
      ArgumentException.ThrowIfNullOrWhiteSpace(value);
      var segments = value.Split(Separator, StringSplitOptions.None);
      if(segments.Any(string.IsNullOrWhiteSpace))
         throw new FormatException($"Source tag '{value}' contains empty segments.");
      return new SourceTag(value, segments);
   }

   public IReadOnlyList<string> Segments => _segments;

   public bool IsContainedIn(SourceTag ancestor) => _value.StartsWith(ancestor._value, StringComparison.Ordinal)
                                                     && (_value.Length == ancestor._value.Length
                                                         || _value[ancestor._value.Length..].StartsWith(Separator, StringComparison.Ordinal));

   public bool Contains(SourceTag descendant) => descendant.IsContainedIn(this);

   public override string ToString() => _value;

   public bool Equals(SourceTag? other) => other is not null && _value == other._value;
   public override bool Equals(object? obj) => Equals(obj as SourceTag);
   public override int GetHashCode() => _value.GetHashCode(StringComparison.Ordinal);

   public static bool operator ==(SourceTag? left, SourceTag? right) => Equals(left, right);
   public static bool operator !=(SourceTag? left, SourceTag? right) => !Equals(left, right);
}
