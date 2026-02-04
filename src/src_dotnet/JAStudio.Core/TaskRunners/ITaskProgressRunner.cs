using System;
using System.Collections.Generic;

namespace JAStudio.Core.TaskRunners;

public interface ITaskProgressRunner : IDisposable
{
    List<TOutput> ProcessWithProgress<TInput, TOutput>(
        List<TInput> items,
        Func<TInput, TOutput> processItem,
        string message,
        bool runGc = false,
        int minimumItemsToGc = 0);

    void SetLabelText(string text);
    void Close();
    TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action);
    void RunGc();
    bool IsHidden();
}

public class InvisibleTaskRunner : ITaskProgressRunner
{
    public InvisibleTaskRunner(string windowTitle, string labelText)
    {
        // Invisible - no UI
    }

    public List<TOutput> ProcessWithProgress<TInput, TOutput>(
        List<TInput> items,
        Func<TInput, TOutput> processItem,
        string message,
        bool runGc = false,
        int minimumItemsToGc = 0)
    {
        var result = new List<TOutput>();
        foreach (var item in items)
        {
            result.Add(processItem(item));
        }
        
        var totalItems = items.Count;
        // TODO: Add StopWatch when ported
        MyLog.Debug($"##--InvisibleTaskRunner--## Finished {message} handled {totalItems} items");
        
        return result;
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

    public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action)
    {
        // TODO: Add StopWatch when ported
        var result = action();
        MyLog.Debug($"##--InvisibleTaskRunner--## Finished {message}");
        return result;
    }

    public bool IsHidden()
    {
        return true;
    }

    public void Dispose()
    {
        Close();
    }
}
