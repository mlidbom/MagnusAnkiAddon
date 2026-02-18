using System;
using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Kanji;

/// <summary>
/// Factory for creating PreRenderingContentRenderer with KanjiNote tag mappings.
/// </summary>
public class KanjiNoteRenderer
{
   public PreRenderingContentRenderer<KanjiNote> CreateRenderer()
   {
      return new PreRenderingContentRenderer<KanjiNote>(new Dictionary<string, Func<KanjiNote, string>>
                                                        {
                                                           ["##BLAZOR_IFRAME##"] = RenderBlazorIframe,
                                                        });
   }

   static string RenderBlazorIframe(KanjiNote note)
   {
      var baseUrl = CardServerUrl.BaseUrl;
      if(baseUrl == null) return "<!-- CardServer not running -->";
      var externalId = note.Collection.GetExternalNoteId(note.GetId());
      return $"""<iframe src="{baseUrl}/card/kanji/back?NoteId={externalId}" style="width:100%;min-height:1600px;border:1px solid #444;border-radius:4px;" frameborder="0"></iframe>""";
   }
}
