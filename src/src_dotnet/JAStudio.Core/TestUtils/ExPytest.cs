using System;
using System.Linq;

namespace JAStudio.Core.TestUtils;

public static class ExPytest
{
    public static bool IsTesting { get; } = AppDomain.CurrentDomain
        .GetAssemblies()
        .Any(a => a.FullName != null && a.FullName.StartsWith("xunit", StringComparison.OrdinalIgnoreCase));
}
