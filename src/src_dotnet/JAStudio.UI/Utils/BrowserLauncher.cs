using System;
using System.Threading.Tasks;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;

namespace JAStudio.UI.Utils;

/// <summary>
/// Utility for opening URLs in the default browser using Avalonia's Launcher API.
/// </summary>
public static class BrowserLauncher
{
    /// <summary>
    /// Opens a URL in the default browser.
    /// </summary>
    public static void OpenUrl(string url)
    {
        // Fire and forget - async void is acceptable for event handlers
        _ = OpenUrlAsync(url);
    }

    /// <summary>
    /// Opens a URL in the default browser asynchronously.
    /// </summary>
    public static async Task<bool> OpenUrlAsync(string url)
    {
        try
        {
            var topLevel = GetTopLevel();
            if (topLevel?.Launcher == null)
            {
                JALogger.Log($"Cannot open URL: Launcher not available");
                return false;
            }

            var uri = new Uri(url);
            var result = await topLevel.Launcher.LaunchUriAsync(uri);
            
            if (!result)
            {
                JALogger.Log($"Failed to open URL: {url} - OS cannot handle the request");
            }
            
            return result;
        }
        catch (Exception ex)
        {
            JALogger.Log($"Failed to open URL: {url}. Error: {ex.Message}");
            return false;
        }
    }

    private static TopLevel? GetTopLevel()
    {
        if (Application.Current?.ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            return desktop.MainWindow != null ? TopLevel.GetTopLevel(desktop.MainWindow) : null;
        }
        return null;
    }
}
