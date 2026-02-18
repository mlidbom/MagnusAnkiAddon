using System;
using System.Threading.Tasks;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;
using JAStudio.Core.Note;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.UI.Web;

/// <summary>
/// Prerenderer that appends rendered content to the incoming HTML rather than replacing tags.
/// Starts rendering in the background when the question is shown, applies the result when the answer is shown.
/// </summary>
public class AppendingPrerenderer<TNote> where TNote : JPNote
{
   readonly Func<TNote, string> _renderMethod;
   Task<string>? _prerenderedTask;

   public AppendingPrerenderer(Func<TNote, string> renderMethod) => _renderMethod = renderMethod;

   public string Render(TNote note, string html, string typeOfDisplay)
   {
      if(DisplayType.IsDisplayingReviewQuestion(typeOfDisplay))
      {
         SchedulePrerender(note);
      } else if(DisplayType.IsDisplayingReviewAnswer(typeOfDisplay) && _prerenderedTask != null)
      {
         html = ApplyPrerendered(html);
      } else if(DisplayType.IsDisplayingAnswer(typeOfDisplay))
      {
         html = RenderSynchronously(note, html);
      }

      return html;
   }

   void SchedulePrerender(TNote note)
   {
      _prerenderedTask = TaskCE.Run(() => RenderWithTiming(note));
   }

   string RenderWithTiming(TNote note)
   {
      using(StopWatch.LogWarningIfSlowerThan(0.5, "prerendering"))
      {
         return _renderMethod(note);
      }
   }

   string ApplyPrerendered(string html)
   {
      using(StopWatch.LogWarningIfSlowerThan(0.01, "fetching_prerendered"))
      {
         var result = html + _prerenderedTask!.Result;
         _prerenderedTask = null;
         return result;
      }
   }

   string RenderSynchronously(TNote note, string html)
   {
      using(StopWatch.LogWarningIfSlowerThan(0.5, "live_rendering"))
      {
         return html + RenderWithTiming(note);
      }
   }
}
