using System;
using JAStudio.Core.LanguageServices.JamdictEx;

namespace JAStudio.Core.Specifications.Fixtures;

public class JamdictCleanupFixture : IDisposable
{
   public void Dispose() => DictLookup.ShutDownJamdict();
}
