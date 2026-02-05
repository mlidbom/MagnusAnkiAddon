using System;
using System.Collections.Generic;
using System.Collections.Frozen;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary;

public static class POSSetManager
{
    private static readonly Dictionary<string, FrozenSet<string>> _posByStr = new();
    private static readonly Dictionary<string, string> _stringInterner = new();

    private static readonly Dictionary<string, List<string>> _remappings = new()
    {
        // Our own harmonizations (for VocabNote usage)
        ["intransitive verb"] = new() { POS.Intransitive },
        ["transitive verb"] = new() { POS.Transitive },
        ["godan"] = new() { POS.GodanVerb },
        ["ichidan"] = new() { POS.IchidanVerb },

        // JMDict POS mappings
        ["な adjective"] = new() { POS.NaAdjective },
        ["noun or participle which takes the aux. verb suru"] = new() { POS.SuruVerb },
        ["noun (common) (futsuumeishi)"] = new() { POS.Noun },
        ["adjectival nouns or quasi-adjectives (keiyodoshi)"] = new() { POS.NaAdjective },
        ["noun, used as a suffix"] = new() { POS.Noun, POS.Suffix },
        ["godan verb with 'u' ending"] = new() { POS.GodanVerb },
        ["godan verb with 'ru' ending"] = new() { POS.GodanVerb },
        ["godan verb with 'mu' ending"] = new() { POS.GodanVerb },
        ["godan verb with 'nu' ending"] = new() { POS.GodanVerb },
        ["godan verb with 'gu' ending"] = new() { POS.GodanVerb },
        ["godan verb with 'ku' ending"] = new() { POS.GodanVerb },
        ["godan verb with 'su' ending"] = new() { POS.GodanVerb },
        ["godan verb with 'bu' ending"] = new() { POS.GodanVerb },
        ["godan verb with 'u' ending (special class)"] = new() { POS.GodanVerb, POS.SpecialClass },
        ["godan verb - -aru special class"] = new() { POS.GodanVerb, POS.SpecialClassAru },
        ["godan verb with 'tsu' ending"] = new() { POS.GodanVerb },
        ["irregular nu verb"] = new() { POS.NuVerb },
        ["godan verb - iku/yuku special class"] = new() { POS.GodanVerb, POS.SpecialClass },
        ["godan verb with 'ru' ending (irregular verb)"] = new() { POS.GodanVerb, POS.Irregular },
        ["ichidan verb"] = new() { POS.IchidanVerb },
        ["ichidan verb - zuru verb (alternative form of -jiru verbs)"] = new() { POS.IchidanVerb, POS.ZuruVerb },
        ["kuru verb - special class"] = new() { POS.KuruVerb, POS.SpecialClass },
        ["yodan verb with 'ru' ending (archaic)"] = new() { POS.YodanVerb },
        ["yodan verb with 'ku' ending (archaic)"] = new() { POS.YodanVerb },
        ["nidan verb (lower class) with 'ru' ending (archaic)"] = new() { POS.NidanVerb },
        ["nidan verb (upper class) with 'ru' ending (archaic)"] = new() { POS.NidanVerb },
        ["adjective (keiyoushi)"] = new() { POS.IAdjective },
        ["adjective (keiyoushi) - yoi/ii class"] = new() { POS.IAdjective },
        ["adverb (fukushi)"] = new() { POS.Adverb },
        ["adverb taking the 'to' particle"] = new() { POS.ToAdverb },
        [POS.Auxiliary] = new() { POS.Auxiliary },
        ["auxiliary adjective"] = new() { POS.IAdjective, POS.Auxiliary },
        ["auxiliary verb"] = new() { POS.Auxiliary },
        [POS.Conjunction] = new() { POS.Conjunction },
        [POS.Copula] = new() { POS.Copula },
        ["expressions (phrases, clauses, etc.)"] = new() { POS.Expression },
        ["interjection (kandoushi)"] = new() { POS.Interjection },
        ["noun, used as a prefix"] = new() { POS.Prefix, POS.Noun },
        ["nouns which may take the genitive case particle 'no'"] = new() { POS.Noun, POS.NoAdjective },
        [POS.Particle] = new() { POS.Particle },
        ["pre-noun adjectival (rentaishi)"] = new() { POS.PreNounAdjectival },
        [POS.Prefix] = new() { POS.Prefix },
        [POS.Pronoun] = new() { POS.Pronoun },
        [POS.Suffix] = new() { POS.Suffix },
        ["suru verb - included"] = new() { POS.SuruVerb },
        [POS.SuruVerb] = new() { POS.SuruVerb },
        ["su verb - precursor to the modern suru"] = new() { POS.SuVerb },
        [POS.Counter] = new() { POS.Counter },
        [POS.Numeric] = new() { POS.Numeric },
        ["noun or verb acting prenominally"] = new() { POS.Prenominal },
        ["suru verb - special class"] = new() { POS.SuruVerb, POS.SpecialClass },
        ["ichidan verb - kureru special class"] = new() { POS.IchidanVerb, POS.SpecialClass },
        ["'taru' adjective"] = new() { POS.TaruAdjective },
    };

    private static HashSet<string> Harmonize(IEnumerable<string> pos)
    {
        var result = new HashSet<string>();
        foreach (var item in pos)
        {
            if (_remappings.TryGetValue(item.ToLower(), out var mapped))
            {
                result.UnionWith(mapped);
            }
            else
            {
                result.Add(item);
            }
        }
        return result;
    }

    private static string AutoIntern(string str)
    {
        if (!_stringInterner.TryGetValue(str, out var interned))
        {
            _stringInterner[str] = str;
            interned = str;
        }
        return interned;
    }

    private static FrozenSet<string> InternFrozenSet(HashSet<string> posValuesSet)
    {
        var posKey = string.Join(", ", posValuesSet.OrderBy(s => s));
        if (!_posByStr.TryGetValue(posKey, out var frozenSet))
        {
            var internedList = posValuesSet.Select(AutoIntern).ToFrozenSet();
            _posByStr[AutoIntern(posKey)] = internedList;
            frozenSet = internedList;
        }
        return frozenSet;
    }

    public static string InternAndHarmonize(string pos)
    {
        var posValuesList = pos.Split(',')
            .Select(s => s.Trim().ToLower())
            .ToList();
        var posValuesSet = Harmonize(posValuesList);
        InternFrozenSet(posValuesSet);
        return string.Join(", ", posValuesSet.OrderBy(s => s));
    }

    public static FrozenSet<string> InternAndHarmonizeFromList(List<string> posList)
    {
        var posValuesSet = Harmonize(posList.Select(p => p.ToLower()));
        return InternFrozenSet(posValuesSet);
    }

    public static FrozenSet<string> Get(string pos)
    {
        return _posByStr[pos];
    }

    public static bool IsTransitiveVerb(FrozenSet<string> posSet)
    {
        return posSet.Contains(POS.Transitive);
    }

    public static bool IsIntransitiveVerb(FrozenSet<string> posSet)
    {
        return posSet.Contains(POS.Intransitive);
    }

    public static bool IsVerb(FrozenSet<string> posSet)
    {
        return posSet.Overlaps(POS.AllVerbPoses);
    }
}
