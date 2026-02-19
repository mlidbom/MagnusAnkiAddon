using System;
using System.Threading.Tasks;
using Compze.Utilities.SystemCE.ThreadingCE.TasksCE;
using JAStudio.Core.Note;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.UI.Web;

/// <summary>
/// Prerenderer that returns a Blazor iframe for both front and back card displays.
/// On review questions, starts prerendering the back side in the background.
/// </summary>
public class AppendingPrerenderer<TNote> where TNote : JPNote
{
   readonly Func<TNote, string, string, string> _renderIframe;
   Task<string>? _prerenderedTask;

   /// <param name="renderIframe">Given a note, card template name, and side (front/back), returns the iframe HTML.</param>
   public AppendingPrerenderer(Func<TNote, string, string, string> renderIframe) => _renderIframe = renderIframe;

   // ReSharper disable once UnusedMember.Global used from python
   public string Render(TNote note, string html, string typeOfDisplay, string cardTemplateName)
   {
      if(!note.Collection.IsInitialized)
         return Mine.AppStillLoadingMessage;

      if(DisplayType.IsDisplayingQuestion(typeOfDisplay))
      {
         if(DisplayType.IsDisplayingReviewQuestion(typeOfDisplay))
            SchedulePrerender(note, cardTemplateName);
         return RenderIframeWithTiming(note, cardTemplateName, "front");
      }

      if(DisplayType.IsDisplayingReviewAnswer(typeOfDisplay) && _prerenderedTask != null)
      {
         html = ApplyPrerendered(html);
      } else if(DisplayType.IsDisplayingAnswer(typeOfDisplay))
      {
         html = RenderSynchronously(note, html, cardTemplateName);
      }

      return html;
   }

   void SchedulePrerender(TNote note, string cardTemplateName)
   {
      _prerenderedTask = TaskCE.Run(() => RenderIframeWithTiming(note, cardTemplateName, "back"));
   }

   string RenderIframeWithTiming(TNote note, string cardTemplateName, string side)
   {
      using(StopWatch.LogWarningIfSlowerThan(0.5, "prerendering"))
      {
         return _renderIframe(note, cardTemplateName, side);
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

   string RenderSynchronously(TNote note, string html, string cardTemplateName)
   {
      using(StopWatch.LogWarningIfSlowerThan(0.5, "live_rendering"))
      {
         return html + RenderIframeWithTiming(note, cardTemplateName, "back");
      }
   }
}
