using System.Collections.Generic;

namespace JAStudio.Core.Configuration;

class TestConfigDictSource : IConfigDictSource
{
   public Dictionary<string, object> Load() => new();
   public void Persist(string json) {}
}
