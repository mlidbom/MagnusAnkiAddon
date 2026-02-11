using System;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Abstraction for a scope-level UI panel that groups child progress panels
/// under a heading. Implemented by the Avalonia UI layer.
/// Core code only interacts with scopes through this interface.
/// </summary>
public interface IScopePanel : IDisposable
{
   /// <summary>
   /// Stop the elapsed timer and return the final elapsed time string.
   /// </summary>
   string GetFinalElapsed();
}
