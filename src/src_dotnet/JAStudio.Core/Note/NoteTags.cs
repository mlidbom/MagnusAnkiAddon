using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note;

public class NoteTags : IEnumerable<Tag>
{
    private readonly JPNote _note;
    private readonly BitFlagsSet _flags;
    private static readonly Dictionary<BitFlagsSet, List<string>> _internedStringLists = new();

    public NoteTags(JPNote note, JPNoteData? data = null)
    {
        _note = note;
        _flags = new BitFlagsSet();

        if (data != null)
        {
            foreach (var tag in data.Tags)
            {
                _flags.SetFlag(Tag.FromName(tag).Id);
            }
        }
    }

    private void Persist()
    {
        _note.Flush();
        _note.OnTagsUpdated();
    }

    public bool Contains(Tag value)
    {
        return _flags.ContainsBit(value.Bit);
    }

    public void Set(Tag tag)
    {
        if (!Contains(tag))
        {
            _flags.SetFlag(tag.Id);
            Persist();
        }
    }

    public void Unset(Tag tag)
    {
        if (Contains(tag))
        {
            _flags.UnsetFlag(tag.Id);
            Persist();
        }
    }

    public void Toggle(Tag tag, bool on)
    {
        if (on)
        {
            Set(tag);
        }
        else
        {
            Unset(tag);
        }
    }

    public IEnumerator<Tag> GetEnumerator()
    {
        return _flags.Select(Tag.FromId).GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    public List<string> ToInternedStringList()
    {
        if (!_internedStringLists.TryGetValue(_flags, out var internedList))
        {
            var sortedNameList = this.Select(t => t.Name).OrderBy(n => n).ToList();
            // Note: Python uses string_auto_interner.auto_intern_qlist() here, but string interning
            // is a Python-specific optimization not needed in C# (per porting rules)
            internedList = sortedNameList;
            _internedStringLists[_flags] = internedList;
        }
        return internedList;
    }
}
