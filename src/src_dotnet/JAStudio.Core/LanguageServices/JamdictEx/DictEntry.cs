using System.Collections.Frozen;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.SysUtils;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.LanguageServices.JamdictEx;

public class SenseEX
{
    public List<string> Glosses { get; }
    public FrozenSet<string> Pos { get; }
    public bool IsKanaOnly { get; }

    public SenseEX(dynamic source)
    {
        // Extract glosses - replace spaces with dashes
        Glosses = new List<string>();
        foreach (var gloss in source.gloss)
        {
            Glosses.Add(((string)gloss.text).Replace(" ", "-"));
        }

        // POSSetManager handles JMDict -> our names mapping and interning
        var posList = new List<string>();
        foreach (var pos in source.pos)
        {
            posList.Add((string)pos);
        }
        Pos = POSSetManager.InternAndHarmonizeFromList(posList);

        // Check if kana only
        var miscList = new List<string>();
        foreach (var misc in source.misc)
        {
            miscList.Add((string)misc);
        }
        IsKanaOnly = miscList.Contains("word usually written using kana alone");
    }

    public bool IsTransitiveVerb() => POSSetManager.IsTransitiveVerb(Pos);
    public bool IsIntransitiveVerb() => POSSetManager.IsIntransitiveVerb(Pos);

    private bool AllGlossesStartWith(string prefix) => Glosses.All(it => it.StartsWith(prefix));

    public bool IsToBeVerb() => AllGlossesStartWith("to-be-");

    public string FormatGlosses()
    {
        if (POSSetManager.IsVerb(Pos))
        {
            var typeMarker = "{?}";
            if (IsTransitiveVerb()) typeMarker = "{}";
            if (IsIntransitiveVerb()) typeMarker = ":";

            var startGroup = "{";
            var endGroup = "}";
            if (Glosses.Count == 1)
            {
                startGroup = "";
                endGroup = "";
            }

            if (IsToBeVerb())
            {
                return $"to-be:{startGroup}{string.Join("/", Glosses.Select(it => RemovePrefix(it, "to-be-")))}{endGroup}";
            }

            if (AllGlossesStartWith("to-"))
            {
                return $"to{typeMarker}{startGroup}{string.Join("/", Glosses.Select(it => RemovePrefix(it, "to-")))}{endGroup}";
            }
        }

        return string.Join("/", Glosses);
    }

    private static string RemovePrefix(string text, string prefix)
    {
        return text.StartsWith(prefix) ? text.Substring(prefix.Length) : text;
    }
}

public class KanaFormEX
{
    public string Text { get; }
    public List<string> PriorityTags { get; }

    public KanaFormEX(dynamic source)
    {
        Text = (string)source.text;
        PriorityTags = new List<string>();
        foreach (var pri in source.pri)
        {
            PriorityTags.Add((string)pri);
        }
    }
}

public class KanjiFormEX
{
    public string Text { get; }
    public List<string> PriorityTags { get; }

    public KanjiFormEX(dynamic source)
    {
        Text = (string)source.text;
        PriorityTags = new List<string>();
        foreach (var pri in source.pri)
        {
            PriorityTags.Add((string)pri);
        }
    }
}

public sealed class DictEntry
{
    public List<KanaFormEX> KanaForms { get; }
    public List<KanjiFormEX> KanjiForms { get; }
    public List<SenseEX> Senses { get; }

    public DictEntry(dynamic source)
    {
        KanaForms = new List<KanaFormEX>();
        foreach (var kanaForm in source.kana_forms)
        {
            KanaForms.Add(new KanaFormEX(kanaForm));
        }

        KanjiForms = new List<KanjiFormEX>();
        foreach (var kanjiForm in source.kanji_forms)
        {
            KanjiForms.Add(new KanjiFormEX(kanjiForm));
        }

        Senses = new List<SenseEX>();
        foreach (var sense in source.senses)
        {
            Senses.Add(new SenseEX(sense));
        }
    }

    public List<string> KanaFormsText() => KanaForms.Select(it => it.Text).ToList();
    public List<string> KanjiFormsText() => KanjiForms.Select(it => it.Text).ToList();

    public bool IsKanaOnly()
    {
        return !KanjiForms.Any() || Senses.Any(sense => sense.IsKanaOnly);
    }

    public static List<DictEntry> Create(IEnumerable<DictEntry> entries)
    {
        return entries.ToList();
    }

    /// <summary>
    /// Creates DictEntry list from Python entries. Must be called while holding the GIL.
    /// </summary>
    internal static List<DictEntry> CreateFromPythonEntries(dynamic pythonEntries)
    {
        var result = new List<DictEntry>();
        foreach (var entry in pythonEntries)
        {
            result.Add(new DictEntry(entry));
        }
        return result;
    }

    public bool HasMatchingKanaForm(string search)
    {
        // TODO: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        search = KanaUtils.KatakanaToHiragana(search);
        return KanaForms.Any(form => search == KanaUtils.KatakanaToHiragana(form.Text));
    }

    public bool HasMatchingKanjiForm(string search)
    {
        // TODO: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        search = KanaUtils.KatakanaToHiragana(search);
        return KanjiForms.Any(form => search == KanaUtils.KatakanaToHiragana(form.Text));
    }

    public HashSet<string> ValidForms(bool forceAllowKanaOnly = false)
    {
        var kanaSet = KanaFormsText().ToHashSet();
        var kanjiSet = KanjiFormsText().ToHashSet();

        if (IsKanaOnly() || forceAllowKanaOnly)
        {
            kanaSet.UnionWith(kanjiSet);
            return kanaSet;
        }
        return kanjiSet;
    }

    public bool IsTransitiveVerb() => Senses.All(it => it.IsTransitiveVerb());
    public bool IsIntransitiveVerb() => Senses.All(it => it.IsIntransitiveVerb());
    public bool IsToBeVerb() => Senses.All(it => it.IsToBeVerb());

    public HashSet<string> PartsOfSpeech()
    {
        var result = new HashSet<string>();
        foreach (var sense in Senses)
        {
            result.UnionWith(sense.Pos);
        }
        return result;
    }

    public string FormatAnswer()
    {
        var defaultFormat = string.Join(" | ", Senses.Select(it => it.FormatGlosses()));

        if (IsToBeVerb())
        {
            return $"to-be: {defaultFormat.Replace("to-be:", "").Replace("{", "").Replace("}", "")}";
        }

        if (IsTransitiveVerb())
        {
            return $"to{{}} {defaultFormat.Replace("to{}", "").Replace("{", "").Replace("}", "")}";
        }

        if (IsIntransitiveVerb())
        {
            if (defaultFormat.Contains("to-be:"))
            {
                return $"to: {defaultFormat.Replace("to-be:", "be-").Replace("to:", "")}";
            }
            else
            {
                return $"to: {defaultFormat.Replace("to:", "").Replace("{", "").Replace("}", "")}";
            }
        }

        return defaultFormat;
    }
}
