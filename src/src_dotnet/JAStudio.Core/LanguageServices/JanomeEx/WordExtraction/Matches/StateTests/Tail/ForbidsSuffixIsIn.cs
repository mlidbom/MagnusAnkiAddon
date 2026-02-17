using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Tail;

static class ForbidsSuffixIsIn
{
   public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
   {
      var suffixes = inspector.Match.Rules.SuffixIsNot;
      if(suffixes.Any() && suffixes.Any(suffix => inspector.Suffix.StartsWith(suffix)))
      {
         return FailedMatchRequirement.Forbids($"suffix_in:{string.Join(",", suffixes)}");
      }

      return null;
   }
}
