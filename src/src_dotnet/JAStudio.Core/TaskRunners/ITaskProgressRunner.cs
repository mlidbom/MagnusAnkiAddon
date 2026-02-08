using System;
using System.Collections.Generic;
using System.Threading.Tasks;

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

    /// <summary>
    /// Async version of <see cref="ProcessWithProgress{TInput,TOutput}"/>.
    /// Runs processing on a background thread while posting progress updates to the UI.
    /// Multiple async operations can run in parallel, each with its own progress display.
    /// </summary>
    Task<List<TOutput>> ProcessWithProgressAsync<TInput, TOutput>(
        List<TInput> items,
        Func<TInput, TOutput> processItem,
        string message);

    /// <summary>
    /// Async version of <see cref="RunOnBackgroundThreadWithSpinningProgressDialog{TResult}"/>.
    /// Runs the action on a background thread with an indeterminate progress indicator.
    /// </summary>
    Task<TResult> RunOnBackgroundThreadAsync<TResult>(string message, Func<TResult> action);
}

