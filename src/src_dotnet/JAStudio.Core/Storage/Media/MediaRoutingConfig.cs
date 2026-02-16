using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Storage.Media;

public record MediaRoutingRule(SourceTag Prefix, string TargetDirectory)
{
   public bool Matches(SourceTag sourceTag) => sourceTag.IsContainedIn(Prefix);
}

public class MediaRoutingConfig(List<MediaRoutingRule> rules)
{
   readonly List<MediaRoutingRule> _rules = rules.OrderByDescending(r => r.Prefix.Segments.Count).ToList();

   public IReadOnlyList<MediaRoutingRule> Rules => _rules;

   public string ResolveDirectory(SourceTag sourceTag) => TryResolveDirectory(sourceTag) ?? throw new InvalidOperationException($"No routing rule matches source tag '{sourceTag}'. Configure a routing rule before importing media.");

   string? TryResolveDirectory(SourceTag sourceTag) => _rules.Where(rule => rule.Matches(sourceTag))
                                                              .Select(it => it.TargetDirectory)
                                                              .FirstOrDefault();
}
