using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using JAStudio.Core.Note;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.UI.Web;

/// <summary>
/// Content rendering with prerendering support.
/// Uses Task.Run for async scheduling instead of Python's ThreadPoolExecutor.
/// </summary>
public class PreRenderingContentRenderer<TNote> where TNote : JPNote
{
    private readonly Dictionary<string, Func<TNote, string>> _renderMethods;
    private Dictionary<string, Task<string>>? _tasks;

    public PreRenderingContentRenderer(Dictionary<string, Func<TNote, string>> renderMethods) => _renderMethods = renderMethods;

    /// <summary>
    /// Main entry point. Dispatches based on display type.
    /// </summary>
    public string Render(TNote note, string html, string typeOfDisplay)
    {
        if (DisplayType.IsDisplayingReviewQuestion(typeOfDisplay))
        {
            SchedulePrerender(note);
        }
        else if (DisplayType.IsDisplayingReviewAnswer(typeOfDisplay) && HasPendingPrerender())
        {
            html = ApplyPrerendered(html);
        }
        else if (DisplayType.IsDisplayingAnswer(typeOfDisplay))
        {
            html = RenderSynchronously(note, html);
        }
        return html;
    }

    /// <summary>
    /// Call when question is shown to start prerendering.
    /// </summary>
    private void SchedulePrerender(TNote note)
    {
        _tasks = _renderMethods.ToDictionary(
            kv => kv.Key,
            kv => Task.Run(() => RenderWithTiming(kv.Value, note, kv.Key))
        );
    }

    private string RenderWithTiming(Func<TNote, string> renderMethod, TNote note, string tag)
    {
        using (StopWatch.LogWarningIfSlowerThan(0.5, $"rendering:{tag}"))
        {
            return renderMethod(note);
        }
    }

    /// <summary>
    /// Apply prerendered results. Call when answer shown after prerendering.
    /// </summary>
    private string ApplyPrerendered(string html)
    {
        if (_tasks == null)
            return html;

        using (StopWatch.LogWarningIfSlowerThan(0.01, "fetching_results"))
        {
            foreach (var (tag, task) in _tasks)
            {
                html = html.Replace(tag, task.Result);
            }
            _tasks = null;
        }
        return html;
    }

    /// <summary>
    /// Render all tags synchronously. For edit/preview mode.
    /// </summary>
    private string RenderSynchronously(TNote note, string html)
    {
        using (StopWatch.LogWarningIfSlowerThan(0.5, "live_rendering"))
        {
            foreach (var (tag, renderMethod) in _renderMethods)
            {
                html = html.Replace(tag, RenderWithTiming(renderMethod, note, tag));
            }
        }
        return html;
    }

    private bool HasPendingPrerender() => _tasks != null;
}
