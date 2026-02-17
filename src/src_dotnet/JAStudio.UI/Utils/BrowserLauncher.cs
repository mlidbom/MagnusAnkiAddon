using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace JAStudio.UI.Utils;

static class BrowserLauncher
{
   public static void OpenUrlInDefaultBrowser(string url)
   {
      if(RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
      {
         Process.Start(new ProcessStartInfo(url) { UseShellExecute = true });
      } else if(RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
      {
         Process.Start("xdg-open", url);
      } else if(RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
      {
         Process.Start("open", url);
      } else
      {
         throw new PlatformNotSupportedException("Cannot open URL: Unsupported platform");
      }
   }
}
