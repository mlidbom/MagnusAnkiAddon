namespace JAStudio.Core;

/// <summary>
/// Provides environment-specific path resolution.
/// Implemented by the host integration layer (e.g. Anki addon) for production,
/// and by test infrastructure for testing.
/// </summary>
public interface IEnvironmentPaths
{
   string AddonRootDir { get; }
}
