using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note;

public class NoteTags : IEnumerable<Tag>
{
    private readonly JPNote _note;
    private readonly HashSet<Tag> _tags = new();
    private static readonly Dictionary<HashSet<Tag>, List<string>> _internedStringLists = new();

    public NoteTags(JPNote note, JPNoteData? data = null)
    {
        _note = note;

        if (data != null)
        {
            foreach (var tagName in data.Tags)
            {
                _tags.Add(Tag.FromName(tagName));
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
        return _tags.Contains(value);
    }

    public void Set(Tag tag)
    {
        if (!Contains(tag))
        {
            _tags.Add(tag);
            Persist();
        }
    }

    public void Unset(Tag tag)
    {
        if (Contains(tag))
        {
            _tags.Remove(tag);
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
        return _tags.GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    public List<string> ToInternedStringList()
    {
        if (!_internedStringLists.TryGetValue(_tags, out var internedList))
        {
            var sortedNameList = this.Select(t => t.Name).OrderBy(n => n).ToList();
            // Note: Python uses string_auto_interner.auto_intern_qlist() here, but string interning
            // is a Python-specific optimization not needed in C# (per porting rules)
            internedList = sortedNameList;
            _internedStringLists[_tags] = internedList;
        }
        return internedList;
    }
}
