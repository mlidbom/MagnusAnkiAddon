using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using JAStudio.Core.Configuration;

namespace JAStudio.Core.TaskRunners;

public class TaskRunner
{
   readonly JapaneseConfig _config;
   internal TaskRunner(JapaneseConfig config) => _config = config;

   Func<string, string, bool, bool, ITaskProgressRunner>? _uiTaskRunnerFactory;
   readonly ThreadLocal<int> _depth = new(() => 0);
   readonly ThreadLocal<ITaskProgressRunner?> _current = new();

   public void SetUiTaskRunnerFactory(Func<string, string, bool, bool, ITaskProgressRunner> factory)
   {
      if(_uiTaskRunnerFactory != null)
      {
         throw new InvalidOperationException("UI task runner factory already set.");
      }

      _uiTaskRunnerFactory = factory;
   }

   internal ITaskProgressRunner Create(string windowTitle, string labelText, bool? visible = null, bool allowCancel = true, bool modal = false)
   {
      visible ??= !App.IsTesting;

      if(!visible.Value)
      {
         return new InvisibleTaskRunner(windowTitle, labelText);
      }

      if(_uiTaskRunnerFactory == null)
      {
         throw new InvalidOperationException("No UI task runner factory set. Set it with TaskRunner.SetUiTaskRunnerFactory().");
      }

      return _uiTaskRunnerFactory(windowTitle, labelText, allowCancel, modal);
   }

   /// <summary>
   /// The one and only way to obtain a task runner.
   /// Returns a scope that implements <see cref="ITaskProgressRunner"/>.
   /// Nested scopes on the same thread share the same progress panel.
   /// Scopes on different threads (e.g. via <see cref="Task.Run"/>) each get their own panel,
   /// enabling parallel tasks to display stacked progress.
   /// </summary>
   public TaskRunnerScope Current(
      string windowTitle,
      string? labelText = null,
      bool forceHide = false,
      bool inhibitGc = false,
      bool forceGc = false,
      bool allowCancel = true,
      bool modal = false) =>
      new(this, _config, windowTitle, labelText, forceHide, inhibitGc, forceGc, allowCancel, modal);

   internal void EnterScope(ITaskProgressRunner runner)
   {
      _depth.Value++;
      if(_depth.Value == 1)
      {
         _current.Value = runner;
      }
   }

   internal void ExitScope(ITaskProgressRunner runner, bool forceGc)
   {
      _depth.Value--;
      if(_depth.Value == 0)
      {
         runner.Close();
         _current.Value = null;
      } else if(forceGc)
      {
         runner.RunGc();
      }
   }

   internal ITaskProgressRunner? GetCurrent() => _current.Value;
}

/// <summary>
/// A scoped task runner obtained from <see cref="TaskRunner.Current"/>.
/// Implements <see cref="ITaskProgressRunner"/> so callers can use it directly
/// without knowing about the underlying runner or other concurrently running tasks.
/// </summary>
public class TaskRunnerScope : IDisposable, ITaskProgressRunner
{
   readonly TaskRunner _taskRunner;
   readonly JapaneseConfig _config;
   readonly ITaskProgressRunner _runner;
   readonly bool _forceGc;
   readonly bool _inhibitGc;

   public TaskRunnerScope(
      TaskRunner taskRunner,
      JapaneseConfig config,
      string windowTitle,
      string? labelText,
      bool forceHide,
      bool inhibitGc,
      bool forceGc,
      bool allowCancel,
      bool modal)
   {
      _taskRunner = taskRunner;
      _config = config;
      _inhibitGc = inhibitGc;
      _forceGc = forceGc;

      var visible = !App.IsTesting && !forceHide;

      if(_taskRunner.GetCurrent() == null)
      {
         _runner = _taskRunner.Create(windowTitle, labelText ?? windowTitle, visible, allowCancel, modal);
         _taskRunner.EnterScope(_runner);

         if(!inhibitGc && (_config.EnableGarbageCollectionDuringBatches.GetValue() || forceGc))
         {
            _runner.RunGc();
         }
      } else
      {
         _runner = _taskRunner.GetCurrent()!;
         _runner.SetLabelText(labelText ?? windowTitle);
      }
   }

   // ── ITaskProgressRunner: delegate to underlying runner ──

   public List<TOutput> ProcessWithProgress<TInput, TOutput>(
      List<TInput> items,
      Func<TInput, TOutput> processItem,
      string message,
      bool runGc = false,
      int minimumItemsToGc = 0)
      => _runner.ProcessWithProgress(items, processItem, message, runGc, minimumItemsToGc);

   public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action)
      => _runner.RunOnBackgroundThreadWithSpinningProgressDialog(message, action);

   public Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(
      List<TInput> items,
      Func<TInput, TOutput> processItem,
      string message)
      => _runner.ProcessWithProgressAsync(items, processItem, message);

   public Task<TResult> RunOnBackgroundThreadAsync<TResult>(string message, Func<TResult> action)
      => _runner.RunOnBackgroundThreadAsync(message, action);

   public void SetLabelText(string text) => _runner.SetLabelText(text);
   public void RunGc() => _runner.RunGc();
   public bool IsHidden() => _runner.IsHidden();

   /// <summary>No-op: runner lifecycle is managed by <see cref="Dispose"/> via ExitScope.</summary>
   public void Close() {}

   public void Dispose()
   {
      if(_taskRunner.GetCurrent() == _runner)
      {
         if(!_inhibitGc && (_config.EnableGarbageCollectionDuringBatches.GetValue() || _forceGc))
         {
            _runner.RunGc();
         }
      }

      _taskRunner.ExitScope(_runner, _forceGc);
   }
}
