using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Minimal base class providing <see cref="INotifyPropertyChanged"/> plumbing.
/// Shared by all framework-agnostic view models in the task runner system.
/// </summary>
public abstract class NotifyPropertyChangedBase : INotifyPropertyChanged
{
   public event PropertyChangedEventHandler? PropertyChanged;

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
