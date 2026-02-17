using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Configuration;

static class ReadingsMappingsParser
{
   public static Dictionary<string, string> Parse(string mappingsString)
   {
      string ParseValuePart(string valuePart)
      {
         if(valuePart.Contains("<read>"))
         {
            return valuePart;
         }

         if(valuePart.Contains(":"))
         {
            var parts = valuePart.Split([':'], 2);
            return $"<read>{parts[0].Trim()}</read>{parts[1]}";
         }

         return $"<read>{valuePart}</read>";
      }

      return mappingsString.Trim().Split('\n')
                           .Where(line => line.Contains(":"))
                           .Select(line => line.Split([':'], 2))
                           .ToDictionary(
                               parts => parts[0].Trim(),
                               parts => ParseValuePart(parts[1].Trim())
                            );
   }
}
