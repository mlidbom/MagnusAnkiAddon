using JAStudio.Core.Note;
using JAStudio.Core.ViewModels.KanjiList;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.UI.Web.Vocab;

public class VocabKanjiListRenderer
{
    readonly TemporaryServiceCollection _services;
    internal VocabKanjiListRenderer(TemporaryServiceCollection services) => _services = services;

    public static string RenderKanjiListFromKanji(List<string> kanjis)
    {
        if (kanjis.Count == 0)
            return "";

        var viewmodel = SentenceKanjiListViewModel.Create(kanjis);

        var kanjiItems = viewmodel.KanjiList.Select(kanji => $$$"""
    <div class="kanji_item {{{string.Join(" ", kanji.Kanji.GetMetaTags())}}}">
        <div class="kanji_main">
            <span class="kanji_kanji clipboard">{{{kanji.Question()}}}</span>
            <span class="kanji_answer">{{{kanji.Answer()}}}</span>
            <span class="kanji_readings">{{{kanji.Readings()}}}</span>
        </div>
        <div class="kanji_mnemonic">{{{kanji.Mnemonic()}}}</div>
    </div>
""");

        return $"""
            <div id="kanji_list" class="page_section">
                <div class="page_section_title">kanji</div>
            {string.Join("\n", kanjiItems)}
            </div>
            """;
    }

    public static string RenderVocabKanjiList(VocabNote vocab)
    {
        return RenderKanjiListFromKanji(vocab.Kanji.ExtractMainFormKanji());
    }
}
