using System;
using System.Linq;

namespace JAStudio.Core.TestUtils;

public class TestEnvDetector
{
    readonly TemporaryServiceCollection _services;
    internal TestEnvDetector(TemporaryServiceCollection services) => _services = services;

    public static bool IsTesting { get; } = AppDomain.CurrentDomain
        .GetAssemblies()
        .Any(a => a.FullName != null && a.FullName.StartsWith("xunit", StringComparison.OrdinalIgnoreCase));
}
