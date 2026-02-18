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

   internal KanjiNoteRenderer(KanjiListRenderer kanjiListRenderer) => _kanjiListRenderer = kanjiListRenderer;

   public PreRenderingContentRenderer<KanjiNote> CreateRenderer()
   {
      return new PreRenderingContentRenderer<KanjiNote>(new Dictionary<string, Func<KanjiNote, string>>
                                                        {
                                                           ["##BLAZOR_IFRAME##"] = _ => RenderBlazorIframe(),
                                                           ["##DEPENDENCIES_LIST##"] = DependenciesRenderer.RenderDependenciesList,
                                                           ["##MNEMONIC##"] = MnemonicRenderer.RenderMnemonic,
                                                           ["##KANJI_READINGS##"] = ReadingsRenderer.RenderKatakanaOnyomi,
                                                           ["##VOCAB_LIST##"] = VocabListRenderer.GenerateVocabHtmlList,
                                                           ["##KANJI_LIST##"] = note => _kanjiListRenderer.KanjiKanjiList(note),
                                                        });
   }

   static string RenderBlazorIframe()
   {
      var baseUrl = CardServerUrl.BaseUrl;
      if(baseUrl == null) return "<!-- CardServer not running -->";
      return $"""<iframe src="{baseUrl}/" style="width:100%;height:120px;border:1px solid #444;border-radius:4px;" frameborder="0"></iframe>""";
   }
}
