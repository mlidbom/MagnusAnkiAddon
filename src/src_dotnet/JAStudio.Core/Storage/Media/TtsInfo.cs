namespace JAStudio.Core.Storage.Media;

public class TtsInfo(string engine, string voice, string version)
{
   public string Engine { get; } = engine;
   public string Voice { get; } = voice;
   public string Version { get; } = version;
}
