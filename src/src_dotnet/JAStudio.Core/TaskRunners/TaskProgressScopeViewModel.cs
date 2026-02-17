using System;
using System.Collections.ObjectModel;
using System.Diagnostics;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Framework-agnostic view model for a scope-level progress panel.
/// Tracks heading, elapsed time, and child <see cref="TaskProgressViewModel"/> instances.
/// The elapsed timer uses <see cref="System.Threading.Timer"/> so it works without
/// any UI framework dependency.
/// </summary>
public class TaskProgressScopeViewModel : NotifyPropertyChangedBase, IDisposable
{
   readonly Stopwatch _stopwatch = Stopwatch.StartNew();
   System.Threading.Timer? _timer;

   public int Depth { get; }

   string _heading;

   public string Heading
   {
      get => _heading;
      set => SetField(ref _heading, value);
   }

   string _elapsedText = "";

   public string ElapsedText
   {
      get => _elapsedText;
      set => SetField(ref _elapsedText, value);
   }

   /// <summary>
   /// Child elements displayed within this scope: <see cref="TaskProgressViewModel"/>
   /// items for individual tasks, and nested <see cref="TaskProgressScopeViewModel"/>
   /// items for child scopes. Add/remove on the UI thread since
   /// <see cref="ObservableCollection{T}"/> is bound to an <c>ItemsControl</c>.
   /// </summary>
   public ObservableCollection<NotifyPropertyChangedBase> Children { get; } = new();

   public TaskProgressScopeViewModel(string heading, int depth)
   {
      _heading = heading;
      Depth = depth;
      _timer = new System.Threading.Timer(_ => UpdateElapsed(), null, TimeSpan.Zero, TimeSpan.FromSeconds(1));
   }

   void UpdateElapsed()
   {
      var elapsed = _stopwatch.Elapsed;
      ElapsedText = $"{elapsed.Hours:D2}:{elapsed.Minutes:D2}:{elapsed.Seconds:D2}";
   }

   public void Dispose()
   {
      _stopwatch.Stop();
      _timer?.Dispose();
      _timer = null;
   }
}
