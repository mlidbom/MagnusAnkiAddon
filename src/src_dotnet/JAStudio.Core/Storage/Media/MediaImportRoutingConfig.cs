using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Storage.Media;

public interface IMediaImportRule
{
   SourceTag Prefix { get; }
}

public class MediaImportRoutingConfig<TRule>(List<TRule> rules) where TRule : IMediaImportRule
{
   readonly List<TRule> _rules = rules.OrderByDescending(r => r.Prefix.Segments.Count).ToList();

   public TRule Resolve(SourceTag sourceTag) =>
      _rules.FirstOrDefault(r => sourceTag.IsContainedIn(r.Prefix))
      ?? throw new InvalidOperationException($"No import routing rule matches source tag '{sourceTag}'. Configure a routing rule before importing media.");
}
