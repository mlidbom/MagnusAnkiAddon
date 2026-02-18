using System.Collections.ObjectModel;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Root view model for the task progress dialog.
/// The UI layer observes <see cref="IsVisible"/> to manage dialog window lifecycle,
/// and binds to <see cref="RootScopes"/> to display the scope panel tree.
/// </summary>
public class TaskProgressDialogViewModel : NotifyPropertyChangedBase
{
   bool _isVisible;

   public bool IsVisible
   {
      get => _isVisible;
      set => SetField(ref _isVisible, value);
   }

   /// <summary>
   /// Top-level scope view models. Each entry becomes a root panel in the dialog.
   /// Nested scopes are children of their parent scope's <see cref="TaskProgressScopeViewModel.Children"/>.
   /// Must be modified on the UI thread (the <see cref="DialogProgressPresenter"/> handles this via <see cref="IUIThreadDispatcher"/>).
   /// </summary>
   public ObservableCollection<TaskProgressScopeViewModel> RootScopes { get; } = [];
}
