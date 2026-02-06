using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Kanji;

public class MnemonicRenderer
{
    readonly TemporaryServiceCollection _services;
    internal MnemonicRenderer(TemporaryServiceCollection services) => _services = services;

    public static string RenderMnemonic(KanjiNote note)
    {
        return note.GetActiveMnemonic();
    }
}
