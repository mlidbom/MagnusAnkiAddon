using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.UI.Web.Vocab;

class RelatedVocabsRenderer
{
   readonly VocabCollection _vocab;
   internal RelatedVocabsRenderer(VocabCollection vocab) => _vocab = vocab;

   public static string CreateClasses(VocabNote vocab) => string.Join(" ", vocab.GetMetaTags());

   static string RenderVocabList(List<VocabNote> vocabList, string title, string cssClass, bool reading = true, bool noSentenceStatistics = true)
   {
      string RenderReadings(VocabNote vocabNote)
      {
         var readings = string.Join(", ", vocabNote.GetReadings());
         return (reading && readings != vocabNote.GetQuestion())
                   ? $"""<span class="clipboard vocabReading">{readings}</span>"""
                   : "";
      }

      if(vocabList.Count == 0)
         return "";

      var vocabEntries = vocabList.Select(vocabNote => $$$"""
                                                          <div class="relatedVocab {{{CreateClasses(vocabNote)}}}">
                                                              <audio src="{{{vocabNote.Audio.PrimaryAudioPath}}}"></audio><a class="play-button"></a>
                                                              <span class="question clipboard">{{{vocabNote.Question.DisambiguationName}}}</span>
                                                              {{{RenderReadings(vocabNote)}}}
                                                              {{{vocabNote.MetaData.MetaTagsHtml(noSentenceStatistics: noSentenceStatistics)}}}
                                                              <span class="meaning"> {{{vocabNote.GetAnswer()}}}</span>
                                                          </div>
                                                          """);

      return $$$"""
                 <div class="relatedVocabListDiv page_section {{{cssClass}}}">
                    <div class="page_section_title">{{{title}}}</div>
                    <div class="vocabHomophonesList">
                        <div>
                            {{{string.Join("\n", vocabEntries)}}}
                        </div>
                    </div>
                </div>
                """;
   }

   public static string GenerateHomophonesHtmlList(VocabNote vocabNote)
   {
      var homophoneNotes = VocabNoteSorting.SortVocabListByStudyingStatus(vocabNote.RelatedNotes.HomophonesNotes());
      if(homophoneNotes.Count > 0)
      {
         homophoneNotes = new List<VocabNote> { vocabNote }.Concat(homophoneNotes).ToList();
      }

      return RenderVocabList(homophoneNotes, "homophones", cssClass: "homophones");
   }

   public static string GenerateSynonymsMeaningHtmlList(VocabNote vocabNote)
   {
      var synonymNotes = vocabNote.RelatedNotes.Synonyms.Notes();
      var perfectSynonyms = vocabNote.RelatedNotes.PerfectSynonyms.Notes().ToHashSet();
      synonymNotes = synonymNotes.Where(synonym => !perfectSynonyms.Contains(synonym)).ToList();
      synonymNotes = VocabNoteSorting.SortVocabListByStudyingStatus(synonymNotes);

      return RenderVocabList(synonymNotes, "synonyms", cssClass: "similar");
   }

   public static string GeneratePerfectSynonymsMeaningHtmlList(VocabNote vocabNote)
   {
      var perfectSynonymNotes = vocabNote.RelatedNotes.PerfectSynonyms.Notes();
      perfectSynonymNotes = VocabNoteSorting.SortVocabListByStudyingStatus(perfectSynonymNotes);

      return RenderVocabList(perfectSynonymNotes, "perfect synonyms, answer automatically synced", cssClass: "similar");
   }

   public static string GenerateAntonymsMeaningHtmlList(VocabNote vocabNote)
   {
      var antonymNotes = vocabNote.RelatedNotes.Antonyms.Notes();
      antonymNotes = VocabNoteSorting.SortVocabListByStudyingStatus(antonymNotes);

      return RenderVocabList(antonymNotes, "antonyms", cssClass: "similar");
   }

   public static string GenerateSeeAlsoHtmlList(VocabNote vocabNote)
   {
      var seeAlso = vocabNote.RelatedNotes.SeeAlso.Notes();
      seeAlso = VocabNoteSorting.SortVocabListByStudyingStatus(seeAlso);

      return RenderVocabList(seeAlso, "see also", cssClass: "similar");
   }

   public string GenerateConfusedWithHtmlList(VocabNote vocabNote)
   {
      var vocabs = vocabNote.RelatedNotes.ConfusedWith.Get();
      var confusedWith = _vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch(vocabs.ToList());
      confusedWith = VocabNoteSorting.SortVocabListByStudyingStatus(confusedWith);

      return RenderVocabList(confusedWith, "confused with", cssClass: "confused_with");
   }

   public string GenerateErgativeTwinHtml(VocabNote vocabNote)
   {
      var ergativeTwin = _vocab.WithFormPreferDisambiguationNameOrExactMatch(vocabNote.RelatedNotes.ErgativeTwin.Get());
      return RenderVocabList(ergativeTwin, "ergative twin", cssClass: "ergative_twin");
   }

   public string GenerateDerivedFrom(VocabNote vocabNote)
   {
      var part = vocabNote.RelatedNotes.DerivedFrom.Get();
      var derivedFrom = _vocab.WithFormPreferDisambiguationNameOrExactMatch(part);
      return RenderVocabList(derivedFrom, "derived from", cssClass: "derived_from");
   }

   public static string GenerateInCompoundsList(VocabNote vocabNote)
   {
      var forms = Conjugator.GetVocabStems(vocabNote).Concat(new[] { vocabNote.Question.Raw }).ToList();

      int PreferCompoundsStartingWithThisVocab(VocabNote vocab)
      {
         var question = vocab.Question.Raw;
         return forms.Any(form => question.StartsWith(form)) ? 0 : 1;
      }

      var inCompounds = vocabNote.RelatedNotes.InCompounds()
                                 .OrderBy(it => it.GetQuestion())
                                 .ThenBy(PreferCompoundsStartingWithThisVocab)
                                 .Take(30)
                                 .ToList();

      return RenderVocabList(inCompounds, "part of compound", cssClass: "in_compound_words");
   }

   public string GenerateStemInCompoundsList(VocabNote vocabNote)
   {
      var masuStem = vocabNote.Question.Stems().MasuStem();
      if(masuStem == null)
         return "";

      var masuStemInCompounds = _vocab.WithCompoundPart(masuStem).Take(30).ToList();
      return RenderVocabList(masuStemInCompounds, "masu stem is part of compound", cssClass: "in_compound_words");
   }

   public string GenerateDerivedList(VocabNote vocabNote)
   {
      var derivedVocabs = _vocab.DerivedFrom(vocabNote.GetQuestion());
      return RenderVocabList(derivedVocabs, "derived vocabulaty", cssClass: "derived_vocabulary");
   }

   public static string GenerateStemVocabs(VocabNote vocabNote) => RenderVocabList(vocabNote.RelatedNotes.StemsNotes().ToList(), "conjugation forms", cssClass: "stem_vocabulary");

   public string GenerateStemOfVocabs(VocabNote vocabNote) => RenderVocabList(_vocab.WithStem(vocabNote.GetQuestion()), "dictionary form", cssClass: "is_stem_of");

   public static string GenerateFormsList(VocabNote vocabNote)
   {
      var forms = vocabNote.Forms.AllListNotesBySentenceCount();
      return forms.Count > 1
                ? RenderVocabList(forms, "forms", cssClass: "forms", noSentenceStatistics: false)
                : "";
   }

   public static string GenerateMetaTags(VocabNote vocabNote) => vocabNote.MetaData.MetaTagsHtml();
}
