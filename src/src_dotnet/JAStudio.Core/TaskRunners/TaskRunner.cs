using System;

namespace JAStudio.Core.TaskRunners;

public static class TaskRunner
{
    private static Func<string, string, bool, bool, ITaskRunner>? _uiTaskRunnerFactory;
    private static int _depth;
    private static ITaskRunner? _current;

    public static void SetUiTaskRunnerFactory(Func<string, string, bool, bool, ITaskRunner> factory)
    {
        if (_uiTaskRunnerFactory != null)
        {
            throw new InvalidOperationException("UI task runner factory already set.");
        }
        _uiTaskRunnerFactory = factory;
    }

    public static ITaskRunner Create(string windowTitle, string labelText, bool? visible = null, bool allowCancel = true, bool modal = false)
    {
        visible ??= !App.IsTesting;
        
        if (!visible.Value)
        {
            return new InvisibleTaskRunner(windowTitle, labelText);
        }

        if (_uiTaskRunnerFactory == null)
        {
            throw new InvalidOperationException("No UI task runner factory set. Set it with TaskRunner.SetUiTaskRunnerFactory().");
        }

        return _uiTaskRunnerFactory(windowTitle, labelText, allowCancel, modal);
    }

    public static TaskRunnerScope Current(
        string windowTitle,
        string? labelText = null,
        bool forceHide = false,
        bool inhibitGc = false,
        bool forceGc = false,
        bool allowCancel = true,
        bool modal = false)
    {
        return new TaskRunnerScope(windowTitle, labelText, forceHide, inhibitGc, forceGc, allowCancel, modal);
    }

    internal static void EnterScope(ITaskRunner runner)
    {
        _depth++;
        if (_depth == 1)
        {
            _current = runner;
        }
    }

    internal static void ExitScope(ITaskRunner runner, bool forceGc)
    {
        _depth--;
        if (_depth == 0)
        {
            runner.Close();
            _current = null;
        }
        else if (forceGc)
        {
            runner.RunGc();
        }
    }

    internal static ITaskRunner? GetCurrent() => _current;
}

public class TaskRunnerScope : IDisposable
{
    private readonly ITaskRunner _runner;
    private readonly bool _forceGc;
    private readonly bool _inhibitGc;

    public TaskRunnerScope(
        string windowTitle,
        string? labelText,
        bool forceHide,
        bool inhibitGc,
        bool forceGc,
        bool allowCancel,
        bool modal)
    {
        _inhibitGc = inhibitGc;
        _forceGc = forceGc;
        
        var visible = !App.IsTesting && !forceHide;
        
        if (TaskRunner.GetCurrent() == null)
        {
            _runner = TaskRunner.Create(windowTitle, labelText ?? windowTitle, visible, allowCancel, modal);
            TaskRunner.EnterScope(_runner);
            
            if (!inhibitGc && (App.Config().EnableGarbageCollectionDuringBatches.GetValue() || forceGc))
            {
                _runner.RunGc();
            }
        }
        else
        {
            _runner = TaskRunner.GetCurrent()!;
            _runner.SetLabelText(labelText ?? windowTitle);
        }
    }
    
    public ITaskRunner Runner => _runner;

    public void Dispose()
    {
        if (TaskRunner.GetCurrent() == _runner)
        {
            if (!_inhibitGc && (App.Config().EnableGarbageCollectionDuringBatches.GetValue() || _forceGc))
            {
                _runner.RunGc();
            }
        }
        TaskRunner.ExitScope(_runner, _forceGc);
    }
}
