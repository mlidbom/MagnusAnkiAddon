using System;

namespace JAStudio.Core.TaskRunners;

public class TaskRunner
{
    readonly TemporaryServiceCollection _services;
    internal TaskRunner(TemporaryServiceCollection services) => _services = services;

    private Func<string, string, bool, bool, ITaskProgressRunner>? _uiTaskRunnerFactory;
    private int _depth;
    private ITaskProgressRunner? _current;

    public void SetUiTaskRunnerFactory(Func<string, string, bool, bool, ITaskProgressRunner> factory)
    {
        if (_uiTaskRunnerFactory != null)
        {
            throw new InvalidOperationException("UI task runner factory already set.");
        }
        _uiTaskRunnerFactory = factory;
    }

    public ITaskProgressRunner Create(string windowTitle, string labelText, bool? visible = null, bool allowCancel = true, bool modal = false)
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

    public TaskRunnerScope Current(
        string windowTitle,
        string? labelText = null,
        bool forceHide = false,
        bool inhibitGc = false,
        bool forceGc = false,
        bool allowCancel = true,
        bool modal = false)
    {
        return new TaskRunnerScope(this, windowTitle, labelText, forceHide, inhibitGc, forceGc, allowCancel, modal);
    }

    internal void EnterScope(ITaskProgressRunner runner)
    {
        _depth++;
        if (_depth == 1)
        {
            _current = runner;
        }
    }

    internal void ExitScope(ITaskProgressRunner runner, bool forceGc)
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

    internal ITaskProgressRunner? GetCurrent() => _current;
}

public class TaskRunnerScope : IDisposable
{
    private readonly TaskRunner _taskRunner;
    private readonly ITaskProgressRunner _runner;
    private readonly bool _forceGc;
    private readonly bool _inhibitGc;

    public TaskRunnerScope(
        TaskRunner taskRunner,
        string windowTitle,
        string? labelText,
        bool forceHide,
        bool inhibitGc,
        bool forceGc,
        bool allowCancel,
        bool modal)
    {
        _taskRunner = taskRunner;
        _inhibitGc = inhibitGc;
        _forceGc = forceGc;
        
        var visible = !App.IsTesting && !forceHide;
        
        if (_taskRunner.GetCurrent() == null)
        {
            _runner = _taskRunner.Create(windowTitle, labelText ?? windowTitle, visible, allowCancel, modal);
            _taskRunner.EnterScope(_runner);
            
            if (!inhibitGc && (App.Config().EnableGarbageCollectionDuringBatches.GetValue() || forceGc))
            {
                _runner.RunGc();
            }
        }
        else
        {
            _runner = _taskRunner.GetCurrent()!;
            _runner.SetLabelText(labelText ?? windowTitle);
        }
    }
    
    public ITaskProgressRunner Runner => _runner;

    public void Dispose()
    {
        if (_taskRunner.GetCurrent() == _runner)
        {
            if (!_inhibitGc && (App.Config().EnableGarbageCollectionDuringBatches.GetValue() || _forceGc))
            {
                _runner.RunGc();
            }
        }
        _taskRunner.ExitScope(_runner, _forceGc);
    }
}
