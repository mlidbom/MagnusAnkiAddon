using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

public sealed class FailedMatchRequirement : MatchRequirement
{
   public string Reason { get; }

   FailedMatchRequirement(string reason) => Reason = reason;

   public override string FailureReason => Reason;
   public override bool IsFulfilled => false;

   public static FailedMatchRequirement Forbids(string message) =>
      new($"forbids::{message}");

   public static FailedMatchRequirement Required(string message) =>
      new($"required::{message}");
}
