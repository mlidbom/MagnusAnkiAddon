using System;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Storage.Media;
using Xunit;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.Storage.Media;

public class When_configuring_media_routing
{
   public class with_multiple_rules : When_configuring_media_routing
   {
      readonly MediaRoutingConfig _config = new(
         [
            new MediaRoutingRule("anime::natsume", "commercial-001"),
            new MediaRoutingRule("anime", "commercial-002")
         ]);

      [XF] public void it_resolves_the_longest_matching_prefix() => _config.ResolveDirectory("anime::natsume::s1::01").Must().Be("commercial-001");
      [XF] public void it_falls_back_to_shorter_prefix() => _config.ResolveDirectory("anime::mushishi::s1::05").Must().Be("commercial-002");
   }

   public class with_no_matching_rule : When_configuring_media_routing
   {
      readonly MediaRoutingConfig _config = new(
         [new MediaRoutingRule("anime", "commercial-001")]);

      [XF] public void it_throws() => Assert.Throws<InvalidOperationException>(() => _config.ResolveDirectory("forvo"));
   }
}
