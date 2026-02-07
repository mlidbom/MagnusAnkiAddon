using System;
using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Sentence;

/// <summary>
/// Factory for creating PreRenderingContentRenderer with SentenceNote tag mappings.
/// </summary>
public static class SentenceNoteRenderer
{
    public static PreRenderingContentRenderer<SentenceNote> CreateRenderer()
    {
        return new PreRenderingContentRenderer<SentenceNote>(new Dictionary<string, Func<SentenceNote, string>>
        {
            ["##USER_QUESTION##"] = note => TemporaryServiceCollection.Instance.SentenceRenderer.RenderUserQuestion(note),
            ["##SOURCE_QUESTION##"] = note => TemporaryServiceCollection.Instance.SentenceRenderer.RenderSourceQuestion(note),
            ["##SENTENCE_ANALYSIS##"] = note => TemporaryServiceCollection.Instance.UdSentenceBreakdownRenderer.RenderSentenceAnalysis(note),
        });
    }
}
