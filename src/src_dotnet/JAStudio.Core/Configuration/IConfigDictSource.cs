using System.Collections.Generic;

namespace JAStudio.Core.Configuration;

public interface IConfigDictSource
{
   Dictionary<string, object> Load();
   void Persist(string json);
}
