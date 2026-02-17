using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using Avalonia.Controls;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace JAStudio.UI.Controls;

partial class StringSetControl : UserControl
{
   public StringSetControl()
   {
      InitializeComponent();
   }
}

/// <summary>
/// ViewModel for a string set control (add/remove chips).
/// </summary>
partial class StringSetControlViewModel : ObservableObject
{
   readonly HashSet<string> _backingSet;
   readonly Window? _parentWindow;
   bool _hasChanges;

   public string Title { get; }

   [ObservableProperty] ObservableCollection<StringChipViewModel> _items = new();

   public StringSetControlViewModel(HashSet<string> backingSet, string title, Window? parentWindow = null)
   {
      _backingSet = backingSet;
      Title = title;
      _parentWindow = parentWindow;
      RefreshItems();
   }

   [RelayCommand] async Task AddAsync()
   {
      if(_parentWindow == null)
         return;

      var dialog = new TextInputDialog
                   {
                      Title = $"Add to {Title}",
                      Prompt = "Enter value:"
                   };

      var result = await dialog.ShowDialog<string?>(_parentWindow);

      if(!string.IsNullOrWhiteSpace(result))
      {
         _backingSet.Add(result);
         _hasChanges = true;
         RefreshItems();
      }
   }

   void RefreshItems()
   {
      Items.Clear();
      foreach(var value in _backingSet.OrderBy(s => s))
      {
         Items.Add(new StringChipViewModel(value, RemoveValue));
      }
   }

   void RemoveValue(string value)
   {
      _backingSet.Remove(value);
      _hasChanges = true;
      RefreshItems();
   }

   public bool HasChanges() => _hasChanges;
}

/// <summary>
/// ViewModel for a single string chip with a remove button.
/// </summary>
partial class StringChipViewModel : ObservableObject
{
   readonly System.Action<string> _onRemove;

   public string Value { get; }

   public StringChipViewModel(string value, System.Action<string> onRemove)
   {
      Value = value;
      _onRemove = onRemove;
   }

   [RelayCommand] void Remove()
   {
      _onRemove(Value);
   }
}

/// <summary>
/// Simple text input dialog.
/// </summary>
class TextInputDialog : Window
{
   public string? Prompt
   {
      get => _promptTextBlock.Text;
      set => _promptTextBlock.Text = value;
   }

   readonly TextBlock _promptTextBlock;

   public TextInputDialog()
   {
      Width = 400;
      Height = 150;
      WindowStartupLocation = WindowStartupLocation.CenterOwner;
      CanResize = false;

      var panel = new StackPanel { Margin = new Avalonia.Thickness(20), Spacing = 15 };

      _promptTextBlock = new TextBlock();
      panel.Children.Add(_promptTextBlock);

      var inputTextBox = new TextBox();
      panel.Children.Add(inputTextBox);

      var buttonPanel = new StackPanel
                        {
                           Orientation = Avalonia.Layout.Orientation.Horizontal,
                           HorizontalAlignment = Avalonia.Layout.HorizontalAlignment.Right,
                           Spacing = 10
                        };

      var okButton = new Button { Content = "OK", Width = 80 };
      okButton.Click += (_, _) => Close(inputTextBox.Text);
      buttonPanel.Children.Add(okButton);

      var cancelButton = new Button { Content = "Cancel", Width = 80 };
      cancelButton.Click += (_, _) => Close(null);
      buttonPanel.Children.Add(cancelButton);

      panel.Children.Add(buttonPanel);

      Content = panel;
   }
}
