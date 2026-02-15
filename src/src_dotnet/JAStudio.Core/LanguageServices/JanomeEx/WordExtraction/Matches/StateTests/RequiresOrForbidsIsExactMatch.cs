using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests;

public static class RequiresOrForbidsSurface
{
   static readonly FailedMatchRequirement RequiredFailure = FailedMatchRequirement.Required("surface");
   static readonly FailedMatchRequirement ForbiddenFailure = FailedMatchRequirement.Forbids("surface");

   public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
   {
      var requirement = inspector.Match.RequiresForbids.Surface;

      if(requirement.IsRequired && !inspector.Variant.IsSurface)
      {
         return RequiredFailure;
      }

      if(requirement.IsForbidden && inspector.Variant.IsSurface && !inspector.BaseEqualsSurface)
      {
         return ForbiddenFailure;
      }

      return null;
   }
}
