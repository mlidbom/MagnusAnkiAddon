using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Kanji;

static class MnemonicRenderer
{
   public static string RenderMnemonic(KanjiNote note) => note.ActiveMnemonic;
}
