using System;

namespace JAStudio.Core.TaskRunners;

public interface ITaskRunner : IDisposable
{
    void SetLabelText(string labelText);
    void RunGc();
    void Close();
}

public class InvisibleTaskRunner : ITaskRunner
{
    public InvisibleTaskRunner(string windowTitle, string labelText)
    {
        // Invisible - no UI
    }

    public void SetLabelText(string labelText)
    {
        // Invisible - no-op
    }

    public void RunGc()
    {
        // TODO: Implement GC management when needed
    }

    public void Close()
    {
        // Invisible - no-op
    }

    public void Dispose()
    {
        Close();
    }
}
