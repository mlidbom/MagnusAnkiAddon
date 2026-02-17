using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// A tree node that records the title and elapsed time of a scope or task.
/// Thread-safe: child entries may be added concurrently from parallel tasks.
/// </summary>
public class TaskLogEntry
{
   readonly ConcurrentQueue<TaskLogEntry> _children = new();
   readonly Stopwatch _stopwatch = Stopwatch.StartNew();

   public string Title { get; }
   public TimeSpan Elapsed { get; private set; }
   public IEnumerable<TaskLogEntry> Children => _children;

   public TaskLogEntry(string title) => Title = title;

   public void AddChild(TaskLogEntry child) => _children.Enqueue(child);

   public void MarkCompleted() => Elapsed = _stopwatch.Elapsed;

   public string FormatTree()
   {
      var sb = new StringBuilder();
      AppendTo(sb, indent: 0, isFirst: true);
      return sb.ToString();
   }

   void AppendTo(StringBuilder sb, int indent, bool isFirst = false)
   {
      if(!isFirst) sb.AppendLine();
      sb.Append(' ', indent * 3);
      sb.Append(Title);
      sb.Append("  [");
      sb.Append(FormatElapsed(Elapsed));
      sb.Append(']');

      foreach(var child in _children)
         child.AppendTo(sb, indent + 1);
   }

   static string FormatElapsed(TimeSpan elapsed)
   {
      if(elapsed.TotalHours >= 1)
         return elapsed.ToString(@"h\:mm\:ss\.f");
      if(elapsed.TotalMinutes >= 1)
         return elapsed.ToString(@"m\:ss\.f");
      if(elapsed.TotalSeconds >= 1)
         return $"{elapsed.TotalSeconds:F2}s";
      return $"{elapsed.TotalMilliseconds:F0}ms";
   }
}
