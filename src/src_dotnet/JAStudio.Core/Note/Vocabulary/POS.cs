using System.Collections.Generic;

namespace JAStudio.Core.Note.Vocabulary;

/// <summary>
/// Canonical POS (Part of Speech) value constants.
/// </summary>
public static class POS
{
   public const string Abbreviation = "abbreviation";
   public const string AdverbialNoun = "adverbial noun";
   public const string Adverbial = "adverbial";
   public const string Numeral = "numeral";
   public const string IndependentNoun = "independent noun";
   public const string Transitive = "transitive";
   public const string Intransitive = "intransitive";
   public const string GodanVerb = "godan verb";
   public const string IchidanVerb = "ichidan verb";
   public const string SuruVerb = "suru verb";
   public const string KuruVerb = "kuru verb";
   public const string NuVerb = "nu verb";
   public const string SuVerb = "su verb";
   public const string YodanVerb = "yodan verb";
   public const string NidanVerb = "nidan verb";
   public const string Noun = "noun";
   public const string ProperNoun = "proper noun";
   public const string NaAdjective = "na-adjective";
   public const string IAdjective = "i-adjective";
   public const string TaruAdjective = "taru-adjective";
   public const string Adverb = "adverb";
   public const string ToAdverb = "to-adverb";
   public const string Expression = "expression";
   public const string Auxiliary = "auxiliary";
   public const string Conjunction = "conjunction";
   public const string Copula = "copula";
   public const string Interjection = "interjection";
   public const string Particle = "particle";
   public const string Prefix = "prefix";
   public const string Suffix = "suffix";
   public const string Pronoun = "pronoun";
   public const string Counter = "counter";
   public const string Numeric = "numeric";
   public const string Prenominal = "prenominal";
   public const string PreNounAdjectival = "pre-noun-adjectival";
   public const string NoAdjective = "no-adjective";
   public const string SpecialClass = "special-class";
   public const string SpecialClassAru = "special-class-aru";
   public const string ZuruVerb = "zuru verb";
   public const string Irregular = "irregular";
   public const string Unknown = "Unknown";
   public const string MasuSuffix = "masu-suffix"; // non-standard, follows the 連用形/masu-stem form of a verb

   public static readonly HashSet<string> AllVerbPoses =
   [
      GodanVerb,
      IchidanVerb,
      SuruVerb,
      KuruVerb,
      NuVerb,
      SuVerb,
      YodanVerb,
      NidanVerb
   ];
}
