using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices;

namespace JAStudio.Core.Note.Collection;

public class KanjiCollection
{
    private readonly IBackendNoteCreator _backendNoteCreator;
    internal readonly KanjiCache Cache;

    public KanjiCollection(IBackendNoteCreator backendNoteCreator)
    {
        _backendNoteCreator = backendNoteCreator;
        Cache = new KanjiCache();
    }

    public List<KanjiNote> All() => Cache.All();

    public KanjiNote? WithIdOrNone(int noteId) => Cache.WithIdOrNone(noteId);

    public List<KanjiNote> WithAnyKanjiIn(List<string> kanjiList)
    {
        return kanjiList.SelectMany(k => Cache.WithQuestion(k)).ToList();
    }

    public KanjiNote? WithKanji(string kanji)
    {
        var results = Cache.WithQuestion(kanji);
        return results.Count == 1 ? results[0] : null;
    }

    public List<KanjiNote> WithRadical(string radical) => Cache.WithRadical(radical);

    public HashSet<KanjiNote> WithReading(string reading)
    {
        var hiraganaReading = KanaUtils.AnythingToHiragana(reading);
        return Cache.ByReading.TryGetValue(hiraganaReading, out var notes) 
            ? notes.ToHashSet() 
            : new HashSet<KanjiNote>();
    }

    public void Add(KanjiNote note)
    {
        _backendNoteCreator.CreateKanji(note, () => Cache.AddToCache(note));
    }
}

public class KanjiSnapshot : CachedNote
{
    public string[] Radicals { get; }
    public string[] Readings { get; }

    public KanjiSnapshot(KanjiNote note) : base(note)
    {
        Radicals = note.GetRadicals().Distinct().ToArray();
        Readings = note.GetReadingsClean().Distinct().ToArray();
    }
}

public class KanjiCache : NoteCache<KanjiNote, KanjiSnapshot>
{
    private readonly Dictionary<string, List<KanjiNote>> _byRadical = new();
    public readonly Dictionary<string, List<KanjiNote>> ByReading = new();

    public KanjiCache() : base(typeof(KanjiNote), (services, data) => new KanjiNote(services, data))
    {
    }

    protected override KanjiSnapshot CreateSnapshot(KanjiNote note)
    {
        return new KanjiSnapshot(note);
    }

    private static void RemoveFirstNoteWithId(List<KanjiNote> noteList, long id)
    {
        for (var i = 0; i < noteList.Count; i++)
        {
            if (noteList[i].GetId() == id)
            {
                noteList.RemoveAt(i);
                return;
            }
        }
        throw new Exception($"Could not find note with id {id} in list");
    }

    protected override void InheritorRemoveFromCache(KanjiNote note, KanjiSnapshot snapshot)
    {
        var id = snapshot.Id;
        foreach (var form in snapshot.Radicals)
        {
            if (_byRadical.TryGetValue(form, out var list))
            {
                RemoveFirstNoteWithId(list, id);
            }
        }
        foreach (var reading in snapshot.Readings)
        {
            if (ByReading.TryGetValue(reading, out var list))
            {
                RemoveFirstNoteWithId(list, id);
            }
        }
    }

    protected override void InheritorAddToCache(KanjiNote note, KanjiSnapshot snapshot)
    {
        foreach (var form in snapshot.Radicals)
        {
            if (!_byRadical.ContainsKey(form))
            {
                _byRadical[form] = new List<KanjiNote>();
            }
            _byRadical[form].Add(note);
        }
        foreach (var reading in snapshot.Readings)
        {
            if (!ByReading.ContainsKey(reading))
            {
                ByReading[reading] = new List<KanjiNote>();
            }
            ByReading[reading].Add(note);
        }
    }

    public List<KanjiNote> WithRadical(string radical)
    {
        return _byRadical.TryGetValue(radical, out var notes) ? notes.ToList() : new List<KanjiNote>();
    }
}
