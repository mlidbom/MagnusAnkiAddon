using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Framework-agnostic view model for a single progress panel.
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

   int _current;
   public int Current
   {
      get => _current;
      set => SetField(ref _current, value);
   }

   int _total;
   public int Total
   {
      get => _total;
      set => SetField(ref _total, value);
   }

   bool _isIndeterminate = true;
   public bool IsIndeterminate
   {
      get => _isIndeterminate;
      set => SetField(ref _isIndeterminate, value);
   }

   bool _isCancelVisible;
   public bool IsCancelVisible
   {
      get => _isCancelVisible;
      set => SetField(ref _isCancelVisible, value);
   }

   string _statsText = "";
   public string StatsText
   {
      get => _statsText;
      set => SetField(ref _statsText, value);
   }

   volatile bool _wasCanceled;
   public bool WasCanceled => _wasCanceled;
   public void RequestCancel() => _wasCanceled = true;

   public void SetProgress(int current, int total)
   {
      IsIndeterminate = false;
      Total = total;
      Current = current;
      StatsText = $"{current}/{total}";
   }

   /// <summary>
   /// Update progress values and compute time estimates in one call.
   /// Consolidates the progress + timing logic that was previously
   /// duplicated across sync and async paths in the runner.
   /// </summary>
   public void UpdateProgressWithTiming(int current, int total, DateTime startTime)
   {
      IsIndeterminate = false;
      Total = total;
      Current = current;

      var elapsedSeconds = (DateTime.Now - startTime).TotalSeconds;
      var estimatedTotalSeconds = current > 0 ? (elapsedSeconds / current) * total : 0;
      var estimatedRemainingSeconds = current > 0 ? estimatedTotalSeconds - elapsedSeconds : 0;

      StatsText = $"{current}/{total}  \u2022  elapsed: {FormatSeconds(elapsedSeconds)}  \u2022  remaining: {FormatSeconds(estimatedRemainingSeconds)}  \u2022  est: {FormatSeconds(estimatedTotalSeconds)}";
   }

   static string FormatSeconds(double seconds)
   {
      var timeSpan = TimeSpan.FromSeconds(seconds);
      return $"{timeSpan.Hours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2}";
   }

   void OnPropertyChanged([CallerMemberName] string? propertyName = null) =>
      PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));

   bool SetField<T>(ref T field, T value, [CallerMemberName] string? propertyName = null)
   {
      if(EqualityComparer<T>.Default.Equals(field, value)) return false;
      field = value;
      OnPropertyChanged(propertyName);
      return true;
   }
}
