using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Kanji;

public static class MnemonicRenderer
{
   public static string RenderMnemonic(KanjiNote note) => note.ActiveMnemonic;
}
