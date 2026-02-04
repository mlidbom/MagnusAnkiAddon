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

