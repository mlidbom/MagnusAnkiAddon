using System;
using System.Diagnostics;

namespace JAStudio.Core.SysUtils;

//porting comment: renamed to avoid collision with assertion libraries assert class
public static class JAAssert
{
    public static void That(bool condition, string? message = null)
    {
        if (!condition)
        {
            throw new InvalidOperationException(message ?? "Assertion failed");
        }
    }
}
