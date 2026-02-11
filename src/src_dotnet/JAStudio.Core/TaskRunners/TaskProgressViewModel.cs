namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Framework-agnostic view model for a spinner-style progress panel.
/// Shows a message, an indeterminate progress bar, and an optional cancel button.
/// Property changes are automatically marshaled to the UI thread by the binding engine.
/// </summary>
public class TaskProgressViewModel : NotifyPropertyChangedBase
{
   string _message = "Processing...";
   public string Message
   {
      get => _message;
      set => SetField(ref _message, value);
   }

   bool _isCancelVisible;
   public bool IsCancelVisible
   {
      get => _isCancelVisible;
      set => SetField(ref _isCancelVisible, value);
   }

   volatile bool _wasCanceled;
   public bool WasCanceled => _wasCanceled;
   public void RequestCancel() => _wasCanceled = true;
}
