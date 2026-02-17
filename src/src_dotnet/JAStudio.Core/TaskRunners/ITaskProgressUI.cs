namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Abstraction for the UI layer's task progress visualization.
/// The production implementation creates Avalonia dialogs and panels.
/// The test implementation returns invisible runners with no UI.
/// Injected into <see cref="TaskRunner"/> at construction time.
/// </summary>
public interface ITaskProgressUI
{
   /// <summary>
   /// Create a scope-level panel that shows a heading and elapsed time.
   /// Parameters: (scopeTitle, nestingDepth, parentScopePanel).
   /// </summary>
   IScopePanel CreateScopePanel(string scopeTitle, int depth, IScopePanel? parentScope);

   /// <summary>
   /// Create a visible task progress runner whose child panels live inside the given scope panel.
   /// </summary>
   ITaskProgressRunner CreateTaskRunner(IScopePanel scopePanel, string labelText, bool allowCancel);

   /// <summary>
   /// Hold the progress dialog open. Called when the outermost task scope is entered.
   /// </summary>
   void HoldDialog();

   /// <summary>
   /// Release a hold on the progress dialog. When all holds are released, the dialog may close.
   /// </summary>
   void ReleaseDialog();
}
