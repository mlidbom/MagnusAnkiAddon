using JAStudio.Core;

namespace JAStudio.Anki;

/// <summary>
/// Provides environment paths by querying the Anki Python environment.
/// </summary>
public class AnkiEnvironmentPaths : IEnvironmentPaths
{
   public string AddonRootDir => AnkiFacade.GetAddonRootDir();
}
