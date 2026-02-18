using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.UI.Web.Vocab;

/// <summary>
/// Creates an AppendingPrerenderer that renders the Blazor iframe for vocab cards.
/// </summary>
public class VocabNoteRenderer
{
   // ReSharper disable once UnusedMember.Global called from python
   public AppendingPrerenderer<VocabNote> CreateRenderer() => new(RenderBlazorIframe, RenderBlazorIframeFront);

   static string RenderBlazorIframe(VocabNote note) => RenderIframe(note, "back");

   static string RenderBlazorIframeFront(VocabNote note) => RenderIframe(note, "front");

   static string RenderIframe(VocabNote note, string side)
   {
      var baseUrl = CardServerUrl.BaseUrl;
      if(baseUrl == null) return "<!-- CardServer not running -->";
      var externalId = note.Collection.GetExternalNoteId(note.GetId());
      return $"""<iframe src="{baseUrl}/card/vocab/{side}?NoteId={externalId}" style="position:fixed;inset:0;width:100%;height:100%;border:none;" frameborder="0"></iframe>""";
   }
}
