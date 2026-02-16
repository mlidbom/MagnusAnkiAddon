using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Storage.Media;

public record MediaRoutingRule(string SourceTagPrefix, string TargetDirectory);

public class MediaRoutingConfig(List<MediaRoutingRule> rules)
{
   readonly List<MediaRoutingRule> _rules = rules.OrderByDescending(r => r.SourceTagPrefix.Length).ToList();

   public IReadOnlyList<MediaRoutingRule> Rules => _rules;

   public string ResolveDirectory(string sourceTag) =>
      _rules.Where(rule => sourceTag.StartsWith(rule.SourceTagPrefix, StringComparison.Ordinal))
            .Select(it => it.TargetDirectory)
            .FirstOrDefault() ??
      throw new InvalidOperationException($"No routing rule matches source tag '{sourceTag}'. Configure a routing rule before importing media.");
}
