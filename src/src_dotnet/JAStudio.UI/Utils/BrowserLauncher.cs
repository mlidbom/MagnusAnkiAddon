using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading.Tasks;

namespace JAStudio.UI.Utils;

/// <summary>
/// Utility for opening URLs in the default browser.
/// Uses OS-specific commands since Avalonia app runs without a MainWindow.
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
                // Windows: use explorer to open URL
                Process.Start(new ProcessStartInfo(url) { UseShellExecute = true });
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
            {
                // Linux: use xdg-open
                Process.Start("xdg-open", url);
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                // macOS: use open
                Process.Start("open", url);
            }
            else
            {
                throw new PlatformNotSupportedException("Cannot open URL: Unsupported platform");
            }
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to open URL: {url}. Error: {ex.Message}");
            throw new InvalidOperationException($"Failed to open URL in browser: {url}", ex);
        }
    }

    /// <summary>
    /// Opens a URL in the default browser asynchronously.
    /// </summary>
    public static async Task<bool> OpenUrlAsync(string url)
    {
        try
        {
            Process? process = null;
            
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                process = Process.Start(new ProcessStartInfo(url) { UseShellExecute = true });
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
            {
                process = Process.Start("xdg-open", url);
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                process = Process.Start("open", url);
            }
            else
            {
                throw new PlatformNotSupportedException("Cannot open URL: Unsupported platform");
            }

            if (process != null)
            {
                await process.WaitForExitAsync();
                return process.ExitCode == 0;
            }
            
            return false;
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to open URL: {url}. Error: {ex.Message}");
            throw new InvalidOperationException($"Failed to open URL in browser: {url}", ex);
        }
    }
}
