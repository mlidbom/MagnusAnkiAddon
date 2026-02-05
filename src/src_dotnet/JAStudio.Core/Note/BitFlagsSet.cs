using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note;

public class BitFlagsSet : IEnumerable<int>
{
    private readonly HashSet<int> _flags = new();

    public bool Contains(int value)
    {
        return _flags.Contains(value);
    }

    public bool ContainsBit(long value)
    {
        // Check if any flag ID in our set, when converted to a bit (1L << id), matches the value
        // This supports the legacy bit-based API
        foreach (var flagId in _flags)
        {
            if ((1L << flagId) == value)
            {
                return true;
            }
        }
        return false;
    }

    public void SetFlag(int flag)
    {
        _flags.Add(flag);
    }

    public void UnsetFlag(int flag)
    {
        _flags.Remove(flag);
    }

    public IEnumerator<int> GetEnumerator()
    {
        return _flags.GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    public override int GetHashCode()
    {
        // Compute hash from sorted flags for consistency
        var hash = new HashCode();
        foreach (var flag in _flags.OrderBy(f => f))
        {
            hash.Add(flag);
        }
        return hash.ToHashCode();
    }

    public override bool Equals(object? obj)
    {
        if (obj is BitFlagsSet other)
        {
            return _flags.SetEquals(other._flags);
        }
        return false;
    }
}
