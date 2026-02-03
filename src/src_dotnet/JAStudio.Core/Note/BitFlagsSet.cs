using System;
using System.Collections;
using System.Collections.Generic;

namespace JAStudio.Core.Note;

public class BitFlagsSet : IEnumerable<int>
{
    private int _bitfield;

    public BitFlagsSet(int bitfield = 0)
    {
        _bitfield = bitfield;
    }

    public bool Contains(int value)
    {
        return (_bitfield & (1 << value)) != 0;
    }

    public bool ContainsBit(int value)
    {
        return (_bitfield & value) != 0;
    }

    public void SetFlag(int flag)
    {
        _bitfield |= (1 << flag);
    }

    public void UnsetFlag(int flag)
    {
        _bitfield &= ~(1 << flag);
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
        return _bitfield;
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
