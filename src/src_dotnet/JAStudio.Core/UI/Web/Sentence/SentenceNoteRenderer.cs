using System;
using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Sentence;

/// <summary>
/// Factory for creating PreRenderingContentRenderer with SentenceNote tag mappings.
/// </summary>
public class SentenceNoteRenderer
{
    readonly SentenceRenderer _sentenceRenderer;
    readonly UdSentenceBreakdownRenderer _udSentenceBreakdownRenderer;

    internal SentenceNoteRenderer(SentenceRenderer sentenceRenderer, UdSentenceBreakdownRenderer udSentenceBreakdownRenderer)
    {
        _sentenceRenderer = sentenceRenderer;
        _udSentenceBreakdownRenderer = udSentenceBreakdownRenderer;
    }

    public PreRenderingContentRenderer<SentenceNote> CreateRenderer()
    {
        return new PreRenderingContentRenderer<SentenceNote>(new Dictionary<string, Func<SentenceNote, string>>
        {
            ["##USER_QUESTION##"] = note => _sentenceRenderer.RenderUserQuestion(note),
            ["##SOURCE_QUESTION##"] = note => _sentenceRenderer.RenderSourceQuestion(note),
            ["##SENTENCE_ANALYSIS##"] = note => _udSentenceBreakdownRenderer.RenderSentenceAnalysis(note),
        });
    }
}
