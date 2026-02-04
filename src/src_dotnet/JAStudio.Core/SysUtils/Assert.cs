using System;
using System.Diagnostics;

namespace JAStudio.Core.SysUtils;

public static class Assert
{
    [Conditional("DEBUG")]
    public static void That(bool condition, string? message = null)
    {
        if (!condition)
        {
            throw new InvalidOperationException(message ?? "Assertion failed");
        }
    }
}
