using System;
using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Vocab;

/// <summary>
/// Factory for creating PreRenderingContentRenderer with VocabNote tag mappings.
/// </summary>
public static class VocabNoteRenderer
{
    public static PreRenderingContentRenderer<VocabNote> CreateRenderer()
    {
        var renderer = TemporaryServiceCollection.Instance.RelatedVocabsRenderer;
        return new PreRenderingContentRenderer<VocabNote>(new Dictionary<string, Func<VocabNote, string>>
        {
            // Related vocabs
            ["##FORMS_LIST##"] = RelatedVocabsRenderer.GenerateFormsList,
            ["##IN_COMPOUNDS##"] = RelatedVocabsRenderer.GenerateInCompoundsList,
            ["##STEM_IN_COMPOUNDS##"] = renderer.GenerateStemInCompoundsList,
            ["##DERIVED_VOCABULARY##"] = renderer.GenerateDerivedList,
            ["##ERGATIVE_TWIN##"] = renderer.GenerateErgativeTwinHtml,
            ["##DERIVED_FROM##"] = renderer.GenerateDerivedFrom,
            ["##HOMOPHONES_LIST##"] = RelatedVocabsRenderer.GenerateHomophonesHtmlList,
            ["##PERFECT_SYNONYMS_LIST##"] = RelatedVocabsRenderer.GeneratePerfectSynonymsMeaningHtmlList,
            ["##SYNONYMS_LIST##"] = RelatedVocabsRenderer.GenerateSynonymsMeaningHtmlList,
            ["##SEE_ALSO_LIST##"] = RelatedVocabsRenderer.GenerateSeeAlsoHtmlList,
            ["##ANTONYMS_LIST##"] = RelatedVocabsRenderer.GenerateAntonymsMeaningHtmlList,
            ["##CONFUSED_WITH_LIST##"] = renderer.GenerateConfusedWithHtmlList,
            ["##VOCAB_META_TAGS_HTML##"] = RelatedVocabsRenderer.GenerateMetaTags,
            ["##VOCAB_CLASSES##"] = RelatedVocabsRenderer.CreateClasses,
            ["##STEM_VOCABULARY##"] = RelatedVocabsRenderer.GenerateStemVocabs,
            ["##IS_STEM_OF##"] = renderer.GenerateStemOfVocabs,
            // Sentences
            ["##IN_SENTENCES##"] = VocabSentencesRenderer.GenerateValidInListHtml,
            ["##MARKED_INVALID_IN_SENTENCES##"] = VocabSentencesRenderer.GenerateMarkedInvalidInListHtml,
            // Compound parts
            ["##VOCAB_COMPOUNDS##"] = CompoundPartsRenderer.GenerateCompounds,
            // Kanji list
            ["##KANJI_LIST##"] = note => TemporaryServiceCollection.Instance.VocabKanjiListRenderer.RenderVocabKanjiList(note),
        });
    }
}
