using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace JAStudio.UI.Utils;

/// <summary>
/// Utility for opening URLs in the default browser.
/// </summary>
public static class BrowserLauncher
{
    /// <summary>
    /// Opens a URL in the default browser.
    /// </summary>
    public static void OpenUrl(string url)
    {
        try
        {
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                Process.Start(new ProcessStartInfo(url) { UseShellExecute = true });
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
            {
                Process.Start("xdg-open", url);
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                Process.Start("open", url);
            }
            else
            {
                throw new PlatformNotSupportedException("Cannot open URL on this platform");
            }
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to open URL: {url}. Error: {ex.Message}");
        }
    }
}
