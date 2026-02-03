using System.Collections.Generic;

namespace JAStudio.Core.Note;

public class Tag
{
    private static readonly HashSet<int> _usedIds = new();
    private static readonly Dictionary<int, Tag> _byId = new();
    private static readonly Dictionary<string, Tag> _byName = new();

    public string Name { get; }
    public int Id { get; }
    public int Bit { get; }

    private Tag(string name)
    {
        var id = _usedIds.Count;

        Name = name;
        Id = id;
        Bit = 1 << id;

        _usedIds.Add(id);
        _byId[id] = this;
        _byName[name] = this;
    }

    public static Tag FromName(string name)
    {
        if (!_byName.TryGetValue(name, out var tag))
        {
            tag = new Tag(name);
        }
        return tag;
    }

    public static Tag FromId(int id)
    {
        return _byId[id];
    }
}
