using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using Avalonia.Threading;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

public class AvaloniaTaskProgressRunner : ITaskProgressRunner
{
    private readonly TaskProgressDialog _dialog;
    private readonly bool _allowCancel;
    private readonly Stopwatch _stopwatch = Stopwatch.StartNew();

    public AvaloniaTaskProgressRunner(string windowTitle, string labelText, bool allowCancel, bool modal)
    {
        _allowCancel = allowCancel;
        
        _dialog = new TaskProgressDialog();
        _dialog.SetTitle(windowTitle);
        _dialog.SetMessage(labelText);
        _dialog.ShowCancelButton(allowCancel);
        
        // Show dialog on UI thread
        Dispatcher.UIThread.Post(() =>
        {
            if (modal)
            {
                // For modal dialogs, we can't use ShowDialog since it's async
                // Just show it as a regular window
                _dialog.Show();
            }
            else
            {
                _dialog.Show();
            }
        });
    }

    public bool IsHidden() => false;

    public void SetLabelText(string text)
    {
        _dialog.SetMessage(text);
    }

    public TResult RunOnBackgroundThreadWithSpinningProgressDialog<TResult>(string message, Func<TResult> action)
    {
        _dialog.SetMessage(message);
        _dialog.SetIndeterminate(true);
        
        var task = Task.Run(action);
        
        // Wait for completion, processing UI events
        while (!task.IsCompleted)
        {
            Dispatcher.UIThread.RunJobs();
            System.Threading.Thread.Sleep(50);
        }
        
        var result = task.Result;
        JALogger.Log($"Finished {message} in {_stopwatch.Elapsed.TotalSeconds:F2}s");
        
        return result;
    }

    public List<TOutput> ProcessWithProgress<TInput, TOutput>(
        List<TInput> items,
        Func<TInput, TOutput> processItem,
        string message,
        bool runGc = false,
        int minimumItemsToGc = 0)
    {
        var totalItems = items.Count;
        var results = new List<TOutput>(totalItems);
        
        _dialog.SetMessage($"{message} 0 of {totalItems}");
        _dialog.SetIndeterminate(false);
        _dialog.SetProgress(0, totalItems);
        
        var startTime = DateTime.Now;
        var lastRefresh = DateTime.Now;

        for (int i = 0; i < totalItems; i++)
        {
            // Check for cancellation
            if (_allowCancel && _dialog.WasCanceled)
            {
                JALogger.Log($"Operation canceled by user after {i} of {totalItems} items");
                break;
            }

            // Process item
            results.Add(processItem(items[i]));
            
            // Update UI periodically (every 100ms or on last item)
            var now = DateTime.Now;
            if ((now - lastRefresh).TotalMilliseconds > 100 || i == totalItems - 1)
            {
                lastRefresh = now;
                _dialog.SetProgress(i + 1, totalItems);
                
                // Calculate time estimates
                if (i > 0)
                {
                    var elapsed = (now - startTime).TotalSeconds;
                    var estimatedTotal = (elapsed / (i + 1)) * totalItems;
                    var estimatedRemaining = estimatedTotal - elapsed;
                    
                    _dialog.SetMessage(
                        $"{message} {i + 1} of {totalItems} " +
                        $"Total: {FormatSeconds(estimatedTotal)} " +
                        $"Elapsed: {FormatSeconds(elapsed)} " +
                        $"Remaining: {FormatSeconds(estimatedRemaining)}");
                }
                
                // Process UI events
                Dispatcher.UIThread.RunJobs();
            }
        }
        
        var finalElapsed = (DateTime.Now - startTime).TotalSeconds;
        JALogger.Log($"Finished {message} in {finalElapsed:F2}s, handled {results.Count} items");
        
        return results;
    }

    private static string FormatSeconds(double seconds)
    {
        var timeSpan = TimeSpan.FromSeconds(seconds);
        return $"{timeSpan.Hours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2}";
    }

    public void RunGc()
    {
        // Skip - Python-specific garbage collection not needed in C#
        // C# has automatic GC that's much more efficient
    }

    public void Close()
    {
        Dispatcher.UIThread.Post(() => _dialog.Close());
    }

    public void Dispose()
    {
        Close();
    }
}
