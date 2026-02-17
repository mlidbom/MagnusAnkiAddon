using Avalonia.Controls;
using CommunityToolkit.Mvvm.ComponentModel;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.UI.Controls;

partial class RequireForbidControl : UserControl
{
   public RequireForbidControl()
   {
      InitializeComponent();
   }
}

/// <summary>
/// ViewModel for a RequireForbid control (three radio buttons: Unset/Required/Forbidden).
/// </summary>
partial class RequireForbidControlViewModel : ObservableObject
{
   readonly RequireForbidFlagField _field;
   readonly bool _initialRequired;
   readonly bool _initialForbidden;

   public string GroupName { get; }
   public bool RepraiseTrigger { get; }

   public RequireForbidControlViewModel(RequireForbidFlagField field, string label, bool reparseTrigger = true)
   {
      _field = field;
      GroupName = $"RequrieForbid_{label.Replace(" ", "_")}";
      RepraiseTrigger = reparseTrigger;

      // Store initial state
      _initialRequired = field.IsConfiguredRequired;
      _initialForbidden = field.IsConfiguredForbidden;

      // Initialize observable properties based on initial state
      if(_initialRequired)
      {
         _isRequired = true;
      } else if(_initialForbidden)
      {
         _isForbidden = true;
      } else
      {
         _isUnset = true;
      }
   }

   [ObservableProperty] bool _isUnset;

   [ObservableProperty] bool _isRequired;

   [ObservableProperty] bool _isForbidden;

   partial void OnIsUnsetChanged(bool value)
   {
      if(value)
      {
         IsRequired = false;
         IsForbidden = false;
         _field.SetRequired(false);
         _field.SetForbidden(false);
      }
   }

   partial void OnIsRequiredChanged(bool value)
   {
      if(value)
      {
         IsUnset = false;
         IsForbidden = false;
         _field.SetRequired(true);
      }
   }

   partial void OnIsForbiddenChanged(bool value)
   {
      if(value)
      {
         IsUnset = false;
         IsRequired = false;
         _field.SetForbidden(true);
      }
   }

   public bool HasChanged()
   {
      var currentRequired = IsRequired;
      var currentForbidden = IsForbidden;
      return currentRequired != _initialRequired || currentForbidden != _initialForbidden;
   }
}
