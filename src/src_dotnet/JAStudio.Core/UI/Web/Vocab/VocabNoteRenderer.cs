using System;
using System.Collections.Generic;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.UI.Web.Vocab;

/// <summary>
/// Factory for creating PreRenderingContentRenderer with VocabNote tag mappings.
/// </summary>
public class VocabNoteRenderer
{
    readonly RelatedVocabsRenderer _relatedVocabsRenderer;
    readonly VocabKanjiListRenderer _vocabKanjiListRenderer;

    internal VocabNoteRenderer(RelatedVocabsRenderer relatedVocabsRenderer, VocabKanjiListRenderer vocabKanjiListRenderer)
    {
        _relatedVocabsRenderer = relatedVocabsRenderer;
        _vocabKanjiListRenderer = vocabKanjiListRenderer;
    }

    public PreRenderingContentRenderer<VocabNote> CreateRenderer()
    {
        return new PreRenderingContentRenderer<VocabNote>(new Dictionary<string, Func<VocabNote, string>>
        {
            // Related vocabs
            ["##FORMS_LIST##"] = RelatedVocabsRenderer.GenerateFormsList,
            ["##IN_COMPOUNDS##"] = RelatedVocabsRenderer.GenerateInCompoundsList,
            ["##STEM_IN_COMPOUNDS##"] = _relatedVocabsRenderer.GenerateStemInCompoundsList,
            ["##DERIVED_VOCABULARY##"] = _relatedVocabsRenderer.GenerateDerivedList,
            ["##ERGATIVE_TWIN##"] = _relatedVocabsRenderer.GenerateErgativeTwinHtml,
            ["##DERIVED_FROM##"] = _relatedVocabsRenderer.GenerateDerivedFrom,
            ["##HOMOPHONES_LIST##"] = RelatedVocabsRenderer.GenerateHomophonesHtmlList,
            ["##PERFECT_SYNONYMS_LIST##"] = RelatedVocabsRenderer.GeneratePerfectSynonymsMeaningHtmlList,
            ["##SYNONYMS_LIST##"] = RelatedVocabsRenderer.GenerateSynonymsMeaningHtmlList,
            ["##SEE_ALSO_LIST##"] = RelatedVocabsRenderer.GenerateSeeAlsoHtmlList,
            ["##ANTONYMS_LIST##"] = RelatedVocabsRenderer.GenerateAntonymsMeaningHtmlList,
            ["##CONFUSED_WITH_LIST##"] = _relatedVocabsRenderer.GenerateConfusedWithHtmlList,
            ["##VOCAB_META_TAGS_HTML##"] = RelatedVocabsRenderer.GenerateMetaTags,
            ["##VOCAB_CLASSES##"] = RelatedVocabsRenderer.CreateClasses,
            ["##STEM_VOCABULARY##"] = RelatedVocabsRenderer.GenerateStemVocabs,
            ["##IS_STEM_OF##"] = _relatedVocabsRenderer.GenerateStemOfVocabs,
            // Sentences
            ["##IN_SENTENCES##"] = VocabSentencesRenderer.GenerateValidInListHtml,
            ["##MARKED_INVALID_IN_SENTENCES##"] = VocabSentencesRenderer.GenerateMarkedInvalidInListHtml,
            // Compound parts
            ["##VOCAB_COMPOUNDS##"] = CompoundPartsRenderer.GenerateCompounds,
            // Kanji list
            ["##KANJI_LIST##"] = note => _vocabKanjiListRenderer.RenderVocabKanjiList(note),
        });
    }
}
