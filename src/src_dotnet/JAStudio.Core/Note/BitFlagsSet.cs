using System;
using System.Collections;
using System.Collections.Generic;

namespace JAStudio.Core.Note;

public class BitFlagsSet : IEnumerable<int>
{
    private long _bitfield;

    public BitFlagsSet(long bitfield = 0)
    {
        _bitfield = bitfield;
    }

    public bool Contains(int value)
    {
        return (_bitfield & (1L << value)) != 0;
    }

    public bool ContainsBit(long value)
    {
        return (_bitfield & value) != 0;
    }

    public void SetFlag(int flag)
    {
        _bitfield |= (1L << flag);
    }

    public void UnsetFlag(int flag)
    {
        _bitfield &= ~(1L << flag);
    }

    public IEnumerator<int> GetEnumerator()
    {
        var bitfield = _bitfield;
        var flag = 0;
        while (bitfield != 0)
        {
            if ((bitfield & 1) != 0)
            {
                yield return flag;
            }
            bitfield >>= 1;
            flag++;
        }
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    public override int GetHashCode()
    {
        return _bitfield.GetHashCode();
    }

    public override bool Equals(object? obj)
    {
        if (obj is BitFlagsSet other)
        {
            return _bitfield == other._bitfield;
        }
        return false;
    }
}
