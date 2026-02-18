using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Kanji;

/// <summary>
/// Creates an AppendingPrerenderer that renders the Blazor iframe for kanji cards.
/// </summary>
public class KanjiNoteRenderer
{
   public AppendingPrerenderer<KanjiNote> CreateRenderer() => new(RenderBlazorIframe);

   static string RenderBlazorIframe(KanjiNote note)
   {
      var baseUrl = CardServerUrl.BaseUrl;
      if(baseUrl == null) return "<!-- CardServer not running -->";
      var externalId = note.Collection.GetExternalNoteId(note.GetId());
      return $"""<iframe src="{baseUrl}/card/kanji/back?NoteId={externalId}" style="width:100%;min-height:1600px;border:1px solid #444;border-radius:4px;" frameborder="0"></iframe>""";
   }
}
