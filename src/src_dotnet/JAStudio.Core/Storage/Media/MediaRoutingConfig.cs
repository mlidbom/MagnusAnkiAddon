using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Storage.Media;

public record MediaRoutingRule(string SourceTagPrefix, string TargetDirectory);

public class MediaRoutingConfig
{
   readonly List<MediaRoutingRule> _rules;
   readonly string _defaultDirectory;

   public MediaRoutingConfig(List<MediaRoutingRule> rules, string defaultDirectory)
   {
      _rules = rules.OrderByDescending(r => r.SourceTagPrefix.Length).ToList();
      _defaultDirectory = defaultDirectory;
   }

   public IReadOnlyList<MediaRoutingRule> Rules => _rules;
   public string DefaultDirectory => _defaultDirectory;

   public string ResolveDirectory(string sourceTag)
   {
      foreach(var rule in _rules)
      {
         if(sourceTag.StartsWith(rule.SourceTagPrefix, StringComparison.Ordinal))
            return rule.TargetDirectory;
      }

      return _defaultDirectory;
   }

   public const string DefaultDirectoryName = "general";

   public static MediaRoutingConfig Default() => new([], DefaultDirectoryName);
}
