using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace JAStudio.Core.Configuration;

class FileReadingsMappingsSource : IReadingsMappingsSource
{
   readonly string _filePath;

   public FileReadingsMappingsSource(IEnvironmentPaths paths) =>
      _filePath = Path.Combine(paths.UserFilesDir, "readings_mappings.txt");

   public Dictionary<string, string> GetMappings() => ReadingsMappingsParser.Parse(ReadRawMappings());
   public string ReadRawMappings() => File.ReadAllText(_filePath);

   public void SaveMappings(string mappings)
   {
      File.WriteAllText(_filePath, mappings);
   }
}
