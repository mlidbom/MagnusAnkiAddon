using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests;

public static class ForbidsIsConfiguredIncorrect
{
   static readonly FailedMatchRequirement Failed = FailedMatchRequirement.Forbids("configured_incorrect");

   public static FailedMatchRequirement? ApplyTo(MatchInspector inspector)
   {
      if(inspector.Configuration.IncorrectMatches.ExcludesAtIndex(inspector.Match.ExclusionForm,
                                                                  inspector.Match.StartIndex))
      {
         return Failed;
      }

      return null;
   }
}
