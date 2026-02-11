using Avalonia.Threading;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.Dialogs;

/// <summary>
/// Adapts <see cref="TaskProgressScopePanel"/> (Avalonia) to <see cref="IScopePanel"/> (Core).
/// </summary>
public class AvaloniaScopePanel : IScopePanel
{
   readonly TaskProgressScopePanel _panel;

   public AvaloniaScopePanel(TaskProgressScopePanel panel) => _panel = panel;

   public TaskProgressScopePanel Panel => _panel;

   public string GetFinalElapsed() => Dispatcher.UIThread.Invoke(() => _panel.GetFinalElapsed());

   public void Dispose() => Dispatcher.UIThread.Post(() => MultiTaskProgressDialog.RemoveScopePanel(_panel));
}
