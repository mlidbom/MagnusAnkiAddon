using System;
using Avalonia.Controls;
using Avalonia.Markup.Xaml;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// A scope-level panel bound to a <see cref="JAStudio.Core.TaskRunners.TaskProgressScopeViewModel"/>.
/// Displays a heading with elapsed time and hosts child progress panels
/// via an <c>ItemsControl</c> bound to the view model's <c>Children</c> collection.
/// Only depth-based visual styling remains in code-behind.
/// </summary>
public partial class TaskProgressScopePanel : UserControl
{
   static readonly string[] DepthBackgrounds = ["#10808080", "#08606080", "#06404060", "#04303050"];

   public TaskProgressScopePanel() : this(1) {}

   public TaskProgressScopePanel(int depth)
   {
      InitializeComponent();
      ApplyDepthStyling(depth);
   }

   void InitializeComponent()
   {
      AvaloniaXamlLoader.Load(this);
   }

   void ApplyDepthStyling(int depth)
   {
      var indent = Math.Max(0, (depth - 1) * 16);
      Margin = new Avalonia.Thickness(indent, 2, 0, 2);

      var border = this.FindControl<Border>("ScopeBorder");
      if(border != null)
      {
         var bgIndex = Math.Min(depth - 1, DepthBackgrounds.Length - 1);
         border.Background = Avalonia.Media.Brush.Parse(DepthBackgrounds[Math.Max(0, bgIndex)]);
      }
   }
}
