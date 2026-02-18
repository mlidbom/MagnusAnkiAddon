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
                                                           ["##BLAZOR_IFRAME##"] = RenderBlazorIframe,
                                                           ["##DEPENDENCIES_LIST##"] = DependenciesRenderer.RenderDependenciesList,
                                                           ["##MNEMONIC##"] = MnemonicRenderer.RenderMnemonic,
                                                           ["##KANJI_READINGS##"] = ReadingsRenderer.RenderKatakanaOnyomi,
                                                           ["##VOCAB_LIST##"] = VocabListRenderer.GenerateVocabHtmlList,
                                                           ["##KANJI_LIST##"] = note => _kanjiListRenderer.KanjiKanjiList(note),
                                                        });
   }

   static string RenderBlazorIframe(KanjiNote note)
   {
      var baseUrl = CardServerUrl.BaseUrl;
      if(baseUrl == null) return "<!-- CardServer not running -->";
      var externalId = note.Collection.GetExternalNoteId(note.GetId());
      return $"""<iframe src="{baseUrl}/card/kanji/back?NoteId={externalId}" style="width:100%;min-height:200px;border:1px solid #444;border-radius:4px;" frameborder="0"></iframe>""";
   }
}
