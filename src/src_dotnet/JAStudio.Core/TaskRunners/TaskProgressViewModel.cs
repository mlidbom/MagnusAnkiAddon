using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Framework-agnostic view model for a spinner-style progress panel.
/// Shows a message, an indeterminate progress bar, and an optional cancel button.
/// Notifies via <see cref="INotifyPropertyChanged"/>; Avalonia's binding
/// engine marshals cross-thread property changes to the UI thread automatically.
/// </summary>
public class TaskProgressViewModel : INotifyPropertyChanged
{
   public event PropertyChangedEventHandler? PropertyChanged;

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

   protected void OnPropertyChanged([CallerMemberName] string? propertyName = null) =>
      PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));

   protected bool SetField<T>(ref T field, T value, [CallerMemberName] string? propertyName = null)
   {
      if(EqualityComparer<T>.Default.Equals(field, value)) return false;
      field = value;
      OnPropertyChanged(propertyName);
      return true;
   }
}
