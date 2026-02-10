using System;
using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Kanji;

/// <summary>
/// Factory for creating PreRenderingContentRenderer with KanjiNote tag mappings.
/// </summary>
public class KanjiNoteRenderer
{
    readonly KanjiListRenderer _kanjiListRenderer;

    internal KanjiNoteRenderer(KanjiListRenderer kanjiListRenderer)
    {
        _kanjiListRenderer = kanjiListRenderer;
    }

    public PreRenderingContentRenderer<KanjiNote> CreateRenderer()
    {
        return new PreRenderingContentRenderer<KanjiNote>(new Dictionary<string, Func<KanjiNote, string>>
        {
            ["##DEPENDENCIES_LIST##"] = DependenciesRenderer.RenderDependenciesList,
            ["##MNEMONIC##"] = MnemonicRenderer.RenderMnemonic,
            ["##KANJI_READINGS##"] = ReadingsRenderer.RenderKatakanaOnyomi,
            ["##VOCAB_LIST##"] = VocabListRenderer.GenerateVocabHtmlList,
            ["##KANJI_LIST##"] = note => _kanjiListRenderer.KanjiKanjiList(note),
        });
    }
}
