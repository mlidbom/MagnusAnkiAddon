using System.Collections.Generic;

namespace JAStudio.Core.Configuration;

public interface IReadingsMappingsSource
{
   Dictionary<string, string> GetMappings();
   string ReadRawMappings();
   void SaveMappings(string mappings);
}
