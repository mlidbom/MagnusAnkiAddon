using System;

namespace JAStudio.UI;

/// <summary>
/// Simple logger for debugging Avalonia UI in Anki context.
/// Uses Console output which appears in Anki's console.
/// </summary>
public static class JALogger
{
    public static void Log(string message)
    {
        try
        {
            Console.WriteLine($"[JAStudio.UI] {message}");
        }
        catch
        {
            // Silently fail if console not available
        }
    }
}
