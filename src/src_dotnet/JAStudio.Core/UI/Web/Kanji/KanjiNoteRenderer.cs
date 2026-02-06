using System;
using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Kanji;

/// <summary>
/// Factory for creating PreRenderingContentRenderer with KanjiNote tag mappings.
/// </summary>
public class KanjiNoteRenderer
{
    readonly TemporaryServiceCollection _services;
    internal KanjiNoteRenderer(TemporaryServiceCollection services) => _services = services;

    public static PreRenderingContentRenderer<KanjiNote> CreateRenderer()
    {
        return new PreRenderingContentRenderer<KanjiNote>(new Dictionary<string, Func<KanjiNote, string>>
        {
            ["##DEPENDENCIES_LIST##"] = DependenciesRenderer.RenderDependenciesList,
            ["##MNEMONIC##"] = MnemonicRenderer.RenderMnemonic,
            ["##KANJI_READINGS##"] = ReadingsRenderer.RenderKatakanaOnyomi,
            ["##VOCAB_LIST##"] = VocabListRenderer.GenerateVocabHtmlList,
            ["##KANJI_LIST##"] = KanjiListRenderer.KanjiKanjiList,
        });
    }
}
