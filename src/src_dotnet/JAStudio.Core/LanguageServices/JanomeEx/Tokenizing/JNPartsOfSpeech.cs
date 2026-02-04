using System;
using System.Collections.Generic;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing;

public class PartOfSpeechDescription
{
    public string Japanese { get; }
    public string English { get; }
    public string Explanation { get; }

    public PartOfSpeechDescription(string japanese, string english, string explanation)
    {
        Japanese = japanese;
        English = english;
        Explanation = explanation;
    }

    public override string ToString() => English;
}

public class JNPartsOfSpeech
{
    private static readonly Dictionary<string, PartOfSpeechDescription> JapaneseToPartOfSpeech = new();
    private static readonly Dictionary<string, JNPartsOfSpeech> FullPartsOfSpeechDictionary = new();

    public PartOfSpeechDescription Level1 { get; }
    public PartOfSpeechDescription Level2 { get; }
    public PartOfSpeechDescription Level3 { get; }
    public PartOfSpeechDescription Level4 { get; }

    static JNPartsOfSpeech()
    {
        // Initialize all part of speech descriptions
        InitializeDescriptions();
        // Initialize all JNPOS static fields
        JNPOS.Initialize();
    }

    private JNPartsOfSpeech(string level1, string level2 = "*", string level3 = "*", string level4 = "*")
    {
        Level1 = JapaneseToPartOfSpeech[level1];
        Level2 = JapaneseToPartOfSpeech[level2];
        Level3 = JapaneseToPartOfSpeech[level3];
        Level4 = JapaneseToPartOfSpeech[level4];
    }

    public static JNPartsOfSpeech Fetch(string unparsed)
    {
        return FullPartsOfSpeechDictionary[unparsed];
    }

    public bool IsNonWordCharacter() => Level1.Japanese == "記号";
    public bool IsNoun() => Level1.Japanese == "名詞";

    public override string ToString()
    {
        return string.Concat(
            "1:" + KanaUtils.PadToLength(Level1.Japanese, 5),
            "2:" + KanaUtils.PadToLength(Level2.Japanese.Replace("*", ""), 6),
            "3:" + KanaUtils.PadToLength(Level3.Japanese.Replace("*", ""), 6),
            "4:" + KanaUtils.PadToLength(Level4.Japanese.Replace("*", ""), 6)
        );
    }

    private static void AddDescription(PartOfSpeechDescription desc)
    {
        JapaneseToPartOfSpeech[desc.Japanese] = desc;
    }

    private static JNPartsOfSpeech AddFullPartOfSpeech(string level1, string level2 = "*", string level3 = "*", string level4 = "*")
    {
        var combined = $"{level1},{level2},{level3},{level4}";
        var partsOfSpeech = new JNPartsOfSpeech(level1, level2, level3, level4);
        FullPartsOfSpeechDictionary[combined] = partsOfSpeech;
        return partsOfSpeech;
    }

    private static void InitializeDescriptions()
    {
        // Level 1
        AddDescription(new PartOfSpeechDescription("名詞", "noun", "Names things or ideas"));
        AddDescription(new PartOfSpeechDescription("形容詞", "i-adjective", "Describes nouns"));
        AddDescription(new PartOfSpeechDescription("連体詞", "pre-noun adjectival / adnominal-adjective", "Modifies nouns directly"));
        AddDescription(new PartOfSpeechDescription("接続詞的", "conjunctive", "words or expressions that function in a manner similar to conjunctions"));
        AddDescription(new PartOfSpeechDescription("動詞", "verb", "Indicates action"));
        AddDescription(new PartOfSpeechDescription("副詞", "adverb", "Modifies verbs/adjectives"));
        AddDescription(new PartOfSpeechDescription("助動詞", "bound-auxiliary", "Modifies verb tense/mood"));
        AddDescription(new PartOfSpeechDescription("助詞", "particle", "Functional word indicating relation such as marking direct object, subject etc"));
        AddDescription(new PartOfSpeechDescription("接続詞", "conjunction", "Connects words/clauses"));
        AddDescription(new PartOfSpeechDescription("感動詞", "interjection", "Expresses emotion"));
        AddDescription(new PartOfSpeechDescription("接頭詞", "prefix", "Added to beginning of words"));
        AddDescription(new PartOfSpeechDescription("フィラー", "filler", "Sound/word filling a pause"));
        AddDescription(new PartOfSpeechDescription("記号", "symbol", "Punctuation, special symbols"));
        AddDescription(new PartOfSpeechDescription("その他", "others", "Miscellaneous, doesn't fit other categories"));

        // Level 2, 3, 4 common
        AddDescription(new PartOfSpeechDescription("*", "*", "Wildcard or general category"));
        AddDescription(new PartOfSpeechDescription("一般", "general", "Generic, non-specific"));
        AddDescription(new PartOfSpeechDescription("サ変接続", "suru-verb", "Nouns convertible into verbs with 'する'"));
        AddDescription(new PartOfSpeechDescription("特殊", "special", "Irregular forms"));
        AddDescription(new PartOfSpeechDescription("副詞可能", "adverbial", "Nouns/verbs that can function as adverbs"));
        AddDescription(new PartOfSpeechDescription("形容動詞語幹", "na-adjective stem", "Base form of na-adjectives"));

        // Level 2
        AddDescription(new PartOfSpeechDescription("自立", "independent", "Not dependent on other words"));
        AddDescription(new PartOfSpeechDescription("動詞接続", "verb-connective", "indicates a form or a word that is used to connect with or modify a verb"));
        AddDescription(new PartOfSpeechDescription("代名詞", "pronoun", "Replaces a noun, e.g., he, she, it"));
        AddDescription(new PartOfSpeechDescription("係助詞", "binding", "Connects words/clauses, e.g., は, も"));
        AddDescription(new PartOfSpeechDescription("読点", "comma", "Punctuation to separate elements"));
        AddDescription(new PartOfSpeechDescription("連体化", "adnominalization", "Turns word into modifier for nouns"));
        AddDescription(new PartOfSpeechDescription("副助詞", "adverbial", "Adverbial particle, modifies verbs"));
        AddDescription(new PartOfSpeechDescription("副助詞／並立助詞／終助詞", "adverbial/coordinating-conjunction/ending", "Various particle types"));
        AddDescription(new PartOfSpeechDescription("形容詞接続", "adjective-connection", "Connects adjectives"));
        AddDescription(new PartOfSpeechDescription("副詞化", "adverbialization", "Turns word into adverb"));
        AddDescription(new PartOfSpeechDescription("間投", "interjection", "Expresses emotion or marks a pause"));
        AddDescription(new PartOfSpeechDescription("非自立", "dependent", "Depends on another word to convey meaning"));
        AddDescription(new PartOfSpeechDescription("括弧閉", "closing-bracket", "Closing bracket punctuation"));
        AddDescription(new PartOfSpeechDescription("括弧開", "opening-bracket", "Opening bracket punctuation"));
        AddDescription(new PartOfSpeechDescription("接尾", "suffix", "Appended to end of words"));
        AddDescription(new PartOfSpeechDescription("接続助詞", "conjunctive", "Connects clauses or sentences"));
        AddDescription(new PartOfSpeechDescription("助詞類接続", "particle-connection", "Connects particles"));
        AddDescription(new PartOfSpeechDescription("数", "numeric", "Numerical expressions"));
        AddDescription(new PartOfSpeechDescription("動詞非自立的", "auxiliary-verb", "Auxiliary verb form"));
        AddDescription(new PartOfSpeechDescription("数接続", "numeric-connection", "Numeric connectors"));
        AddDescription(new PartOfSpeechDescription("句点", "period", "Ending punctuation mark"));
        AddDescription(new PartOfSpeechDescription("格助詞", "case-particle", "Indicates grammatical case"));
        AddDescription(new PartOfSpeechDescription("アルファベット", "alphabet", "Alphabetical characters"));
        AddDescription(new PartOfSpeechDescription("ナイ形容詞語幹", "negative-adjective-stem", "Negative adjective stem form"));
        AddDescription(new PartOfSpeechDescription("空白", "space", "Whitespace or blank space"));
        AddDescription(new PartOfSpeechDescription("名詞接続", "noun-connection", "Noun connectors"));
        AddDescription(new PartOfSpeechDescription("終助詞", "sentence-ending", "Ends the sentence"));
        AddDescription(new PartOfSpeechDescription("固有名詞", "proper-noun", "Names of specific entities, like Tokyo"));
        AddDescription(new PartOfSpeechDescription("並立助詞", "coordinating-conjunction", "Connects equal grammatical items, e.g., and, or"));
        AddDescription(new PartOfSpeechDescription("引用文字列", "quoted-character-string", "quoted-character-string"));

        // Level 3
        AddDescription(new PartOfSpeechDescription("助数詞", "counter", "Counting words, e.g., つ, 本"));
        AddDescription(new PartOfSpeechDescription("連語", "compound", "Compound words, two or more words combined"));
        AddDescription(new PartOfSpeechDescription("人名", "person-name", "Names of people"));
        AddDescription(new PartOfSpeechDescription("地域", "region", "Names of regions, cities, countries"));
        AddDescription(new PartOfSpeechDescription("引用", "quotation", "Quotation or citation"));
        AddDescription(new PartOfSpeechDescription("組織", "organization", "Names of organizations, companies"));
        AddDescription(new PartOfSpeechDescription("助動詞語幹", "auxiliary-verb-stem", "Base form of auxiliary verbs"));
        AddDescription(new PartOfSpeechDescription("縮約", "contraction", "Contracted forms, e.g., can't, don't"));

        // Level 4
        AddDescription(new PartOfSpeechDescription("名", "first-name", "Given names"));
        AddDescription(new PartOfSpeechDescription("姓", "surname", "Family names or surnames"));
        AddDescription(new PartOfSpeechDescription("国", "country", "Names of countries"));
    }
}

public static class JNPOS
{
    public static JNPartsOfSpeech Filler { get; private set; } = null!;
    public static JNPartsOfSpeech BoundAuxiliary { get; private set; } = null!;
    public static JNPartsOfSpeech PreNounAdjectival { get; private set; } = null!;
    public static JNPartsOfSpeech Interjection { get; private set; } = null!;
    public static JNPartsOfSpeech Conjunction { get; private set; } = null!;

    internal static void Initialize()
    {
        Filler = JNPartsOfSpeech.Fetch("フィラー,*,*,*");
        BoundAuxiliary = JNPartsOfSpeech.Fetch("助動詞,*,*,*");
        PreNounAdjectival = JNPartsOfSpeech.Fetch("連体詞,*,*,*");
        Interjection = JNPartsOfSpeech.Fetch("感動詞,*,*,*");
        Conjunction = JNPartsOfSpeech.Fetch("接続詞,*,*,*");

        Other.Initialize();
        Adverb.Initialize();
        Particle.Initialize();
        Verb.Initialize();
        Noun.Initialize();
        Adjective.Initialize();
        Prefix.Initialize();
        Symbol.Initialize();
    }

    public static class Other
    {
        public static JNPartsOfSpeech Interjection { get; private set; } = null!;

        internal static void Initialize()
        {
            Interjection = JNPartsOfSpeech.Fetch("その他,間投,*,*");
        }
    }

    public static class Adverb
    {
        public static JNPartsOfSpeech General { get; private set; } = null!;
        public static JNPartsOfSpeech ParticleConnection { get; private set; } = null!;

        internal static void Initialize()
        {
            General = JNPartsOfSpeech.Fetch("副詞,一般,*,*");
            ParticleConnection = JNPartsOfSpeech.Fetch("副詞,助詞類接続,*,*");
        }
    }

    public static class Particle
    {
        public static JNPartsOfSpeech CoordinatingConjunction { get; private set; } = null!;
        public static JNPartsOfSpeech Binding { get; private set; } = null!;
        public static JNPartsOfSpeech Adverbial { get; private set; } = null!;
        public static JNPartsOfSpeech AdverbialCoordinatingEnding { get; private set; } = null!;
        public static JNPartsOfSpeech Adverbialization { get; private set; } = null!;
        public static JNPartsOfSpeech Conjunctive { get; private set; } = null!;
        public static JNPartsOfSpeech Special { get; private set; } = null!;
        public static JNPartsOfSpeech SentenceEnding { get; private set; } = null!;
        public static JNPartsOfSpeech Adnominalization { get; private set; } = null!;

        internal static void Initialize()
        {
            CoordinatingConjunction = JNPartsOfSpeech.Fetch("助詞,並立助詞,*,*");
            Binding = JNPartsOfSpeech.Fetch("助詞,係助詞,*,*");
            Adverbial = JNPartsOfSpeech.Fetch("助詞,副助詞,*,*");
            AdverbialCoordinatingEnding = JNPartsOfSpeech.Fetch("助詞,副助詞／並立助詞／終助詞,*,*");
            Adverbialization = JNPartsOfSpeech.Fetch("助詞,副詞化,*,*");
            Conjunctive = JNPartsOfSpeech.Fetch("助詞,接続助詞,*,*");
            Special = JNPartsOfSpeech.Fetch("助詞,特殊,*,*");
            SentenceEnding = JNPartsOfSpeech.Fetch("助詞,終助詞,*,*");
            Adnominalization = JNPartsOfSpeech.Fetch("助詞,連体化,*,*");

            CaseMarking.Initialize();
        }

        public static class CaseMarking
        {
            public static JNPartsOfSpeech General { get; private set; } = null!;
            public static JNPartsOfSpeech Quotation { get; private set; } = null!;
            public static JNPartsOfSpeech Compound { get; private set; } = null!;

            internal static void Initialize()
            {
                General = JNPartsOfSpeech.Fetch("助詞,格助詞,一般,*");
                Quotation = JNPartsOfSpeech.Fetch("助詞,格助詞,引用,*");
                Compound = JNPartsOfSpeech.Fetch("助詞,格助詞,連語,*");
            }
        }
    }

    public static class Verb
    {
        public static JNPartsOfSpeech Suffix { get; private set; } = null!;
        public static JNPartsOfSpeech Independent { get; private set; } = null!;
        public static JNPartsOfSpeech Dependent { get; private set; } = null!;
        public static HashSet<JNPartsOfSpeech> AllTypes { get; private set; } = null!;

        internal static void Initialize()
        {
            Suffix = JNPartsOfSpeech.Fetch("動詞,接尾,*,*");
            Independent = JNPartsOfSpeech.Fetch("動詞,自立,*,*");
            Dependent = JNPartsOfSpeech.Fetch("動詞,非自立,*,*");
            AllTypes = new HashSet<JNPartsOfSpeech> { Independent, Dependent, Suffix };
        }
    }

    public static class Noun
    {
        public static JNPartsOfSpeech SuruVerb { get; private set; } = null!;
        public static JNPartsOfSpeech NegativeAdjectiveStem { get; private set; } = null!;
        public static JNPartsOfSpeech General { get; private set; } = null!;
        public static JNPartsOfSpeech Adverbial { get; private set; } = null!;
        public static JNPartsOfSpeech AuxiliaryVerb { get; private set; } = null!;
        public static JNPartsOfSpeech NaAdjectiveStem { get; private set; } = null!;
        public static JNPartsOfSpeech Numeric { get; private set; } = null!;
        public static JNPartsOfSpeech Conjunctive { get; private set; } = null!;
        public static JNPartsOfSpeech QuotedCharacterString { get; private set; } = null!;

        internal static void Initialize()
        {
            SuruVerb = JNPartsOfSpeech.Fetch("名詞,サ変接続,*,*");
            NegativeAdjectiveStem = JNPartsOfSpeech.Fetch("名詞,ナイ形容詞語幹,*,*");
            General = JNPartsOfSpeech.Fetch("名詞,一般,*,*");
            Adverbial = JNPartsOfSpeech.Fetch("名詞,副詞可能,*,*");
            AuxiliaryVerb = JNPartsOfSpeech.Fetch("名詞,動詞非自立的,*,*");
            NaAdjectiveStem = JNPartsOfSpeech.Fetch("名詞,形容動詞語幹,*,*");
            Numeric = JNPartsOfSpeech.Fetch("名詞,数,*,*");
            Conjunctive = JNPartsOfSpeech.Fetch("名詞,接続詞的,*,*");
            QuotedCharacterString = JNPartsOfSpeech.Fetch("名詞,引用文字列,*,*");

            Pronoun.Initialize();
            ProperNoun.Initialize();
            Suffix.Initialize();
            Special.Initialize();
            Dependent.Initialize();
        }

        public static class Pronoun
        {
            public static JNPartsOfSpeech General { get; private set; } = null!;
            public static JNPartsOfSpeech Contracted { get; private set; } = null!;

            internal static void Initialize()
            {
                General = JNPartsOfSpeech.Fetch("名詞,代名詞,一般,*");
                Contracted = JNPartsOfSpeech.Fetch("名詞,代名詞,縮約,*");
            }
        }

        public static class ProperNoun
        {
            public static JNPartsOfSpeech General { get; private set; } = null!;
            public static JNPartsOfSpeech Organization { get; private set; } = null!;

            internal static void Initialize()
            {
                General = JNPartsOfSpeech.Fetch("名詞,固有名詞,一般,*");
                Organization = JNPartsOfSpeech.Fetch("名詞,固有名詞,組織,*");

                Person.Initialize();
                Location.Initialize();
            }

            public static class Person
            {
                public static JNPartsOfSpeech General { get; private set; } = null!;
                public static JNPartsOfSpeech Firstname { get; private set; } = null!;
                public static JNPartsOfSpeech Surname { get; private set; } = null!;

                internal static void Initialize()
                {
                    General = JNPartsOfSpeech.Fetch("名詞,固有名詞,人名,一般");
                    Firstname = JNPartsOfSpeech.Fetch("名詞,固有名詞,人名,名");
                    Surname = JNPartsOfSpeech.Fetch("名詞,固有名詞,人名,姓");
                }
            }

            public static class Location
            {
                public static JNPartsOfSpeech General { get; private set; } = null!;
                public static JNPartsOfSpeech Country { get; private set; } = null!;

                internal static void Initialize()
                {
                    General = JNPartsOfSpeech.Fetch("名詞,固有名詞,地域,一般");
                    Country = JNPartsOfSpeech.Fetch("名詞,固有名詞,地域,国");
                }
            }
        }

        public static class Suffix
        {
            public static JNPartsOfSpeech SuruVerbConnection { get; private set; } = null!;
            public static JNPartsOfSpeech General { get; private set; } = null!;
            public static JNPartsOfSpeech PersonsName { get; private set; } = null!;
            public static JNPartsOfSpeech Adverbial { get; private set; } = null!;
            public static JNPartsOfSpeech AuxiliaryVerbStem { get; private set; } = null!;
            public static JNPartsOfSpeech Counter { get; private set; } = null!;
            public static JNPartsOfSpeech Region { get; private set; } = null!;
            public static JNPartsOfSpeech NaAdjectiveStem { get; private set; } = null!;
            public static JNPartsOfSpeech Special { get; private set; } = null!;

            internal static void Initialize()
            {
                SuruVerbConnection = JNPartsOfSpeech.Fetch("名詞,接尾,サ変接続,*");
                General = JNPartsOfSpeech.Fetch("名詞,接尾,一般,*");
                PersonsName = JNPartsOfSpeech.Fetch("名詞,接尾,人名,*");
                Adverbial = JNPartsOfSpeech.Fetch("名詞,接尾,副詞可能,*");
                AuxiliaryVerbStem = JNPartsOfSpeech.Fetch("名詞,接尾,助動詞語幹,*");
                Counter = JNPartsOfSpeech.Fetch("名詞,接尾,助数詞,*");
                Region = JNPartsOfSpeech.Fetch("名詞,接尾,地域,*");
                NaAdjectiveStem = JNPartsOfSpeech.Fetch("名詞,接尾,形容動詞語幹,*");
                Special = JNPartsOfSpeech.Fetch("名詞,接尾,特殊,*");
            }
        }

        public static class Special
        {
            public static JNPartsOfSpeech AuxiliaryVerbStem { get; private set; } = null!;

            internal static void Initialize()
            {
                AuxiliaryVerbStem = JNPartsOfSpeech.Fetch("名詞,特殊,助動詞語幹,*");
            }
        }

        public static class Dependent
        {
            public static JNPartsOfSpeech General { get; private set; } = null!;
            public static JNPartsOfSpeech Adverbial { get; private set; } = null!;
            public static JNPartsOfSpeech AuxiliaryVerbStem { get; private set; } = null!;
            public static JNPartsOfSpeech NaAdjectiveStem { get; private set; } = null!;

            internal static void Initialize()
            {
                General = JNPartsOfSpeech.Fetch("名詞,非自立,一般,*");
                Adverbial = JNPartsOfSpeech.Fetch("名詞,非自立,副詞可能,*");
                AuxiliaryVerbStem = JNPartsOfSpeech.Fetch("名詞,非自立,助動詞語幹,*");
                NaAdjectiveStem = JNPartsOfSpeech.Fetch("名詞,非自立,形容動詞語幹,*");
            }
        }
    }

    public static class Adjective
    {
        public static JNPartsOfSpeech Suffix { get; private set; } = null!;
        public static JNPartsOfSpeech Independent { get; private set; } = null!;
        public static JNPartsOfSpeech Dependent { get; private set; } = null!;
        public static HashSet<JNPartsOfSpeech> AllTypes { get; private set; } = null!;

        internal static void Initialize()
        {
            Suffix = JNPartsOfSpeech.Fetch("形容詞,接尾,*,*");
            Independent = JNPartsOfSpeech.Fetch("形容詞,自立,*,*");
            Dependent = JNPartsOfSpeech.Fetch("形容詞,非自立,*,*");
            AllTypes = new HashSet<JNPartsOfSpeech> { Independent, Dependent, Suffix };
        }
    }

    public static class Prefix
    {
        public static JNPartsOfSpeech Noun { get; private set; } = null!;
        public static JNPartsOfSpeech Adjective { get; private set; } = null!;
        public static JNPartsOfSpeech Number { get; private set; } = null!;
        public static JNPartsOfSpeech VerbConnective { get; private set; } = null!;

        internal static void Initialize()
        {
            Noun = JNPartsOfSpeech.Fetch("接頭詞,名詞接続,*,*");
            Adjective = JNPartsOfSpeech.Fetch("接頭詞,形容詞接続,*,*");
            Number = JNPartsOfSpeech.Fetch("接頭詞,数接続,*,*");
            VerbConnective = JNPartsOfSpeech.Fetch("接頭詞,動詞接続,*,*");
        }
    }

    public static class Symbol
    {
        public static JNPartsOfSpeech Alphabet { get; private set; } = null!;
        public static JNPartsOfSpeech General { get; private set; } = null!;
        public static JNPartsOfSpeech Period { get; private set; } = null!;
        public static JNPartsOfSpeech ClosingBracket { get; private set; } = null!;
        public static JNPartsOfSpeech OpeningBracket { get; private set; } = null!;
        public static JNPartsOfSpeech Space { get; private set; } = null!;
        public static JNPartsOfSpeech Comma { get; private set; } = null!;

        internal static void Initialize()
        {
            Alphabet = JNPartsOfSpeech.Fetch("記号,アルファベット,*,*");
            General = JNPartsOfSpeech.Fetch("記号,一般,*,*");
            Period = JNPartsOfSpeech.Fetch("記号,句点,*,*");
            ClosingBracket = JNPartsOfSpeech.Fetch("記号,括弧閉,*,*");
            OpeningBracket = JNPartsOfSpeech.Fetch("記号,括弧開,*,*");
            Space = JNPartsOfSpeech.Fetch("記号,空白,*,*");
            Comma = JNPartsOfSpeech.Fetch("記号,読点,*,*");
        }
    }
}
