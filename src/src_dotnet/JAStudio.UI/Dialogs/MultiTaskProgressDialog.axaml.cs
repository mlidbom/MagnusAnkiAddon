using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using Avalonia.Threading;
using JAStudio.Core.TaskRunners;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Dialogs;

partial class MultiTaskProgressDialog : Window
{
   static MultiTaskProgressDialog? _instance;
   static int _holdCount;

   MultiTaskProgressDialog() => InitializeComponent();

   void InitializeComponent()
   {
      AvaloniaXamlLoader.Load(this);
   }

   StackPanel Container => this.FindControl<StackPanel>("PanelContainer")!;

   /// <summary> Hold the dialog open even when all panels have been removed. Call once when the outermost task scope is entered. Must be called on the UI thread. </summary>
   internal static void Hold()
   {
      Dispatcher.UIThread.VerifyAccess();
      _holdCount++;
      EnsureVisible();
   }

   /// <summary> Release a hold. When the hold count reaches zero and no panels remain, the dialog is closed. </summary>
   internal static void Release()
   {
      Dispatcher.UIThread.VerifyAccess();
      _holdCount--;
      CloseIfEmpty();
   }

   /// <summary>Create a new top-level scope panel and add it to the shared dialog. Opens the dialog if it is not already visible. Must be called on the UI thread. </summary>
   internal static TaskProgressScopePanel CreateScopePanel(TaskProgressScopeViewModel viewModel, int depth)
   {
      Dispatcher.UIThread.VerifyAccess();
      EnsureVisible();

      var scopePanel = new TaskProgressScopePanel(depth) { DataContext = viewModel };
      _instance!.Container.Children.Add(scopePanel);
      return scopePanel;
   }

   /// <summary> Remove a scope panel from the shared dialog. Closes the dialog when the last panel is removed and no holds are active. Must be called on the UI thread. </summary>
   internal static void RemoveScopePanel(TaskProgressScopePanel scopePanel)
   {
      Dispatcher.UIThread.VerifyAccess();

      if(_instance == null) return;

      _instance.Container.Children.Remove(scopePanel);
      CloseIfEmpty();
   }

   static void EnsureVisible()
   {
      if(_instance is not { IsVisible: true })
      {
         _instance = new MultiTaskProgressDialog().ShowNearCursor();
      }
   }

   static void CloseIfEmpty()
   {
      if(_instance != null && _holdCount <= 0 && _instance.Container.Children.Count == 0)
      {
         _instance.Close();
         _instance = null;
      }
   }
}
