using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;

/// <summary>
/// Base class providing access to VocabMatch context and helper properties.
/// This class holds a reference to a VocabMatch and provides convenient
/// properties for inspecting the match's word, variant, location, and surrounding context.
/// </summary>
public class VocabMatchInspector : MatchInspector
{
   VocabMatchingRulesConfigurationRequiresForbidsFlags? _requiresForbids;

   public VocabMatchInspector(VocabMatch match) : base(match) {}

   public new VocabMatch Match => (VocabMatch)base.Match;

   public VocabMatchingRulesConfigurationRequiresForbidsFlags RequiresForbids
   {
      get
      {
         if(_requiresForbids == null)
         {
            _requiresForbids = Match.RequiresForbids;
         }

         return _requiresForbids;
      }
   }

   public bool PreviousLocationIsIrrealis =>
      PreviousLocation != null && PreviousLocation.Token.IsIrrealis;

   public bool PreviousLocationIsGodan =>
      PreviousLocation != null && PreviousLocation.Token.IsGodanVerb;

   public bool PreviousLocationIsIchidan =>
      PreviousLocation != null && PreviousLocation.Token.IsIchidanVerb;

   public bool BaseEqualsSurface => Word.SurfaceForm == Word.BaseForm;
}
