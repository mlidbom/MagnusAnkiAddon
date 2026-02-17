namespace JAStudio.Core.TaskRunners;

/// <summary>
/// No-op implementation for tests and headless environments.
/// All methods return invisible runners with no UI.
/// </summary>
class HeadlessTaskProgressUI : ITaskProgressUI
{
   public IScopePanel CreateScopePanel(string scopeTitle, int depth, IScopePanel? parentScope) =>
      throw new System.InvalidOperationException("Headless mode should never create visible scope panels.");

   public ITaskProgressRunner CreateTaskRunner(IScopePanel scopePanel, string labelText, bool allowCancel) =>
      throw new System.InvalidOperationException("Headless mode should never create visible task runners.");

   public void HoldDialog() {}
   public void ReleaseDialog() {}
}
