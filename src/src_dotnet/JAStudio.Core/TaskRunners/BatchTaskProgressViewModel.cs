using System;
using System.Diagnostics;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// View model for a batch progress panel that processes a collection of items.
/// Extends <see cref="TaskProgressViewModel"/> with determinate progress tracking:
/// current/total counts and time estimates.
/// </summary>
public class BatchTaskProgressViewModel : TaskProgressViewModel
{
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

   string _statsText = "";

   public string StatsText
   {
      get => _statsText;
      set => SetField(ref _statsText, value);
   }

   public void SetProgress(int current, int total)
   {
      Total = total;
      Current = current;
      StatsText = $"{current}/{total}";
   }

   /// <summary>
   /// Update progress values and compute time estimates in one call.
   /// Uses a monotonic <see cref="Stopwatch"/> for accurate elapsed time.
   /// </summary>
   public void UpdateProgressWithTiming(int current, int total, Stopwatch stopwatch)
   {
      Total = total;
      Current = current;

      var elapsedSeconds = stopwatch.Elapsed.TotalSeconds;
      var estimatedTotalSeconds = current > 0 ? (elapsedSeconds / current) * total : 0;
      var estimatedRemainingSeconds = current > 0 ? estimatedTotalSeconds - elapsedSeconds : 0;

      StatsText = $"{current}/{total}  \u2022  elapsed: {FormatSeconds(elapsedSeconds)}  \u2022  remaining: {FormatSeconds(estimatedRemainingSeconds)}  \u2022  est: {FormatSeconds(estimatedTotalSeconds)}";
   }

   static string FormatSeconds(double seconds)
   {
      var timeSpan = TimeSpan.FromSeconds(seconds);
      return $"{timeSpan.Hours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2}";
   }
}
