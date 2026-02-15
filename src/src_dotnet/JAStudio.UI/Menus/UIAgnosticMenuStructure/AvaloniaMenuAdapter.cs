using System.Collections.Generic;
using Avalonia.Controls;
using Compze.Utilities.Logging;

namespace JAStudio.UI.Menus.UIAgnosticMenuStructure;

/// <summary>
/// Converts UI-agnostic MenuItem specifications to Avalonia MenuItems.
/// This is a thin adapter - all menu structure/logic lives in the spec classes.
/// </summary>
public static class AvaloniaMenuAdapter
{
   static readonly ILogger Log = CompzeLogger.For(typeof(AvaloniaMenuAdapter));

   /// <summary>
   /// Convert a single MenuItem spec to an Avalonia MenuItem.
   /// Recursively builds submenus.
   /// </summary>
   public static MenuItem ToAvalonia(SpecMenuItem spec)
   {
      if(spec.Kind == SpecMenuItemKind.Separator)
      {
         // Avalonia uses a special Separator control, not a MenuItem
         // Caller should check Kind and use new Separator() instead
         Log.Info("Warning: ToAvalonia called on separator - caller should handle separators directly");
         return new MenuItem { Header = "-", IsEnabled = false };
      }

      var avaloniaItem = new MenuItem
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

      switch(spec.Kind)
      {
         case SpecMenuItemKind.Command:
            avaloniaItem.Click += (_, _) => { spec.Action(); };
            break;

         case SpecMenuItemKind.Submenu:
            foreach(var childSpec in spec.Children)
            {
               if(!childSpec.IsVisible)
                  continue;

               if(childSpec.Kind == SpecMenuItemKind.Separator)
                  avaloniaItem.Items.Add(new Separator());
               else
                  avaloniaItem.Items.Add(ToAvalonia(childSpec));
            }

            break;
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

         if(spec.Kind == SpecMenuItemKind.Separator)
            result.Add(new Separator());
         else
            result.Add(ToAvalonia(spec));
      }

      return result;
   }
}

/// <summary>
/// Helper to parse keyboard shortcut strings into Avalonia KeyGestures.
/// </summary>
static class KeyGestureParser
{
   public static Avalonia.Input.KeyGesture? Parse(string shortcutText) => Avalonia.Input.KeyGesture.Parse(shortcutText);
}
