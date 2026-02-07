using System.Collections.Generic;
using Avalonia.Controls;

namespace JAStudio.UI.Menus.UIAgnosticMenuStructure;

/// <summary>
/// Converts UI-agnostic MenuItem specifications to Avalonia MenuItems.
/// This is a thin adapter - all menu structure/logic lives in the spec classes.
/// </summary>
public static class AvaloniaMenuAdapter
{
   /// <summary>
   /// Convert a single MenuItem spec to an Avalonia MenuItem.
   /// Recursively builds submenus.
   /// </summary>
   public static Avalonia.Controls.MenuItem ToAvalonia(SpecMenuItem spec)
   {
      if(spec.IsSeparator)
      {
         // Avalonia uses a special Separator control, not a MenuItem
         // Caller should check IsSeparator and use new Separator() instead
         JALogger.Log("Warning: ToAvalonia called on separator - caller should handle separators directly");
         return new Avalonia.Controls.MenuItem { Header = "-", IsEnabled = false };
      }

      var avaloniaItem = new Avalonia.Controls.MenuItem
                         {
                            Header = spec.Name,
                            IsEnabled = spec.IsEnabled,
                            IsVisible = spec.IsVisible
                         };

      // Add keyboard shortcut display text if present
      if(!string.IsNullOrEmpty(spec.KeyboardShortcut))
      {
         avaloniaItem.InputGesture = KeyGestureParser.Parse(spec.KeyboardShortcut);
      }

      // Wire up command action
      if(spec.Action != null)
      {
         avaloniaItem.Click += (sender, args) =>
         {
            spec.Action();
         };
      }

      // Recursively build submenu children
      if(spec.Children != null && spec.Children.Count > 0)
      {
         foreach(var childSpec in spec.Children)
         {
            if(!childSpec.IsVisible)
               continue; // Skip invisible items

            if(childSpec.IsSeparator)
            {
               avaloniaItem.Items.Add(new Separator());
            } else
            {
               avaloniaItem.Items.Add(ToAvalonia(childSpec));
            }
         }
      }

      return avaloniaItem;
   }

   /// <summary>
   /// Convert a list of MenuItem specs to Avalonia MenuItems.
   /// Useful for building entire menu structures at once.
   /// </summary>
   public static IEnumerable<object> ToAvaloniaList(IEnumerable<SpecMenuItem> specs)
   {
      var result = new List<object>();
      foreach(var spec in specs)
      {
         if(!spec.IsVisible)
            continue;

         if(spec.IsSeparator)
         {
            result.Add(new Separator());
         } else
         {
            result.Add(ToAvalonia(spec));
         }
      }

      return result;
   }
}

/// <summary>
/// Helper to parse keyboard shortcut strings into Avalonia KeyGestures.
/// </summary>
internal static class KeyGestureParser
{
   public static Avalonia.Input.KeyGesture? Parse(string shortcutText) => Avalonia.Input.KeyGesture.Parse(shortcutText);
}
