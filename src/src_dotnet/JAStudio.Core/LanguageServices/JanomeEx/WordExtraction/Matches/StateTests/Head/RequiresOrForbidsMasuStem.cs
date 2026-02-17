using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

static class RequiresOrForbidsMasuStem
{
   static readonly FailedMatchRequirement RequiredReason = FailedMatchRequirement.Required("masu-stem");
   static readonly FailedMatchRequirement ForbiddenReason = FailedMatchRequirement.Forbids("masu-stem");

   public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
   {
      if(inspector.RequiresForbids.MasuStem.IsRequired && !inspector.HasMasuStem)
      {
         return RequiredReason;
      }

      if(inspector.RequiresForbids.MasuStem.IsForbidden && inspector.HasMasuStem)
      {
         return ForbiddenReason;
      }

      return null;
   }
}
