using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Kanji;

/// <summary>
/// Creates an AppendingPrerenderer that renders the Blazor iframe for kanji cards.
/// </summary>
public class KanjiNoteRenderer
{
   // ReSharper disable once UnusedMember.Global called from python
   public AppendingPrerenderer<KanjiNote> CreateRenderer() => new(RenderBlazorIframe, RenderBlazorIframeFront);

   static string RenderBlazorIframe(KanjiNote note) => RenderIframe(note, "back", "");

   static string RenderBlazorIframeFront(KanjiNote note) => RenderIframe(note, "front", "");

   static string RenderIframe(KanjiNote note, string side, string extraStyle)
   {
      var baseUrl = CardServerUrl.BaseUrl;
      if(baseUrl == null) return "<!-- CardServer not running -->";
      var externalId = note.Collection.GetExternalNoteId(note.GetId());
      return $"""<iframe src="{baseUrl}/card/kanji/{side}?NoteId={externalId}" style="width:100%;height:100%;{extraStyle}" frameborder="0"></iframe>""";
   }
}
