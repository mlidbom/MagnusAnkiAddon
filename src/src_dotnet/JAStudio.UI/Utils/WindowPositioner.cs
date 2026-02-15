using System;
using System.Runtime.InteropServices;
using Avalonia;
using Avalonia.Controls;

namespace JAStudio.UI.Utils;

/// <summary>
/// Positions Avalonia windows near the current mouse cursor, clamped to the screen's working area.
/// This ensures dialogs appear on the same monitor the user is interacting with,
/// rather than always centering on the primary monitor.
/// </summary>
public static class WindowPositioner
{
   [DllImport("user32.dll")]
   [return: MarshalAs(UnmanagedType.Bool)]
   static extern bool GetCursorPos(out POINT lpPoint);

   [StructLayout(LayoutKind.Sequential)]
   struct POINT
   {
      public int X;
      public int Y;
   }

   /// <summary>
   /// Position a window centered on the current mouse cursor, clamped to the screen's working area.
   /// Must be called after the window is constructed but before <see cref="Window.Show"/>.
   /// Sets <see cref="Window.WindowStartupLocation"/> to <see cref="WindowStartupLocation.Manual"/>.
   /// </summary>
   public static Window PositionNearCursor(this Window window)
   {
      window.WindowStartupLocation = WindowStartupLocation.Manual;

      if(!GetCursorPos(out var cursor))
         return window;

      // Position is refined in the Opened event so we know the actual rendered size.
      // Set an initial position at the cursor to avoid a flash at (0,0).
      window.Position = new PixelPoint(cursor.X, cursor.Y);

      window.Opened += OnOpened;

      void OnOpened(object? sender, EventArgs e)
      {
         window.Opened -= OnOpened;
         ApplyPosition(window, cursor.X, cursor.Y);
      }

      return window;
   }

   /// <summary>
   /// Reposition an already-visible window near the current mouse cursor.
   /// Useful for singleton/toggle dialogs that need repositioning each time they are shown.
   /// </summary>
   public static void RepositionNearCursor(Window window)
   {
      if(!GetCursorPos(out var cursor))
         return;

      ApplyPosition(window, cursor.X, cursor.Y);
   }

   static void ApplyPosition(Window window, int cursorX, int cursorY)
   {
      var scaling = GetScalingForScreen(window, cursorX, cursorY);

      // Window dimensions in physical (device) pixels.
      // Use Bounds if available (window already rendered), otherwise fall back to Width/Height properties.
      var logicalWidth = window.Bounds.Width > 0 ? window.Bounds.Width : window.Width;
      var logicalHeight = window.Bounds.Height > 0 ? window.Bounds.Height : window.Height;
      var windowWidthPx = (int)(logicalWidth * scaling);
      var windowHeightPx = (int)(logicalHeight * scaling);

      // Center the window on the cursor
      var x = cursorX - windowWidthPx / 2;
      var y = cursorY - windowHeightPx / 2;

      // Clamp to the working area of the screen the cursor is on
      var workingArea = GetWorkingArea(window, cursorX, cursorY);
      if(workingArea.HasValue)
      {
         var wa = workingArea.Value;
         x = Math.Clamp(x, wa.X, Math.Max(wa.X, wa.X + wa.Width - windowWidthPx));
         y = Math.Clamp(y, wa.Y, Math.Max(wa.Y, wa.Y + wa.Height - windowHeightPx));
      }

      window.Position = new PixelPoint(x, y);
   }

   static PixelRect? GetWorkingArea(Window window, int cursorX, int cursorY)
   {
      var cursorPoint = new PixelPoint(cursorX, cursorY);

      foreach(var screen in window.Screens.All)
      {
         if(screen.Bounds.Contains(cursorPoint))
            return screen.WorkingArea;
      }

      return window.Screens.Primary?.WorkingArea;
   }

   static double GetScalingForScreen(Window window, int cursorX, int cursorY)
   {
      var cursorPoint = new PixelPoint(cursorX, cursorY);

      foreach(var screen in window.Screens.All)
      {
         if(screen.Bounds.Contains(cursorPoint))
            return screen.Scaling;
      }

      return window.Screens.Primary?.Scaling ?? 1.0;
   }
}
