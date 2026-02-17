using System;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace JAStudio.Core.Storage.Media;

public static class SidecarSerializer
{
   public const string AudioSidecarExtension = ".audio.json";
   public const string ImageSidecarExtension = ".image.json";
   const string SidecarJsonExtension = ".json";
   public const string AudioSidecarGlob = "*" + AudioSidecarExtension;
   public const string ImageSidecarGlob = "*" + ImageSidecarExtension;

   static readonly JsonSerializerOptions Options = new()
                                                   {
                                                      WriteIndented = true,
                                                      PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                                                      DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingDefault,
                                                      Converters =
                                                      {
                                                         new JsonStringEnumConverter(JsonNamingPolicy.CamelCase),
                                                         new NoteIdJsonConverter(),
                                                         new MediaFileIdJsonConverter(),
                                                         new SourceTagJsonConverter()
                                                      }
                                                   };

   public static string SerializeAudio(AudioAttachment attachment) => JsonSerializer.Serialize(attachment, Options);

   public static string SerializeImage(ImageAttachment attachment) => JsonSerializer.Serialize(attachment, Options);

   public static AudioAttachment DeserializeAudio(string json) =>
      JsonSerializer.Deserialize<AudioAttachment>(json, Options)
   ?? throw new JsonException("Failed to deserialize AudioAttachment");

   public static ImageAttachment DeserializeImage(string json) =>
      JsonSerializer.Deserialize<ImageAttachment>(json, Options)
   ?? throw new JsonException("Failed to deserialize ImageAttachment");

   public static bool IsSidecarFile(string filePath) => filePath.EndsWith(SidecarJsonExtension, StringComparison.OrdinalIgnoreCase);

   public static string BuildAudioSidecarPath(string mediaFilePath)
   {
      var dir = Path.GetDirectoryName(mediaFilePath) ?? string.Empty;
      var id = Path.GetFileNameWithoutExtension(mediaFilePath);
      return Path.Combine(dir, $"{id}{AudioSidecarExtension}");
   }

   public static string BuildImageSidecarPath(string mediaFilePath)
   {
      var dir = Path.GetDirectoryName(mediaFilePath) ?? string.Empty;
      var id = Path.GetFileNameWithoutExtension(mediaFilePath);
      return Path.Combine(dir, $"{id}{ImageSidecarExtension}");
   }

   public static void WriteAudioSidecar(string sidecarPath, AudioAttachment attachment) =>
      File.WriteAllText(sidecarPath, SerializeAudio(attachment));

   public static void WriteImageSidecar(string sidecarPath, ImageAttachment attachment) =>
      File.WriteAllText(sidecarPath, SerializeImage(attachment));

   public static AudioAttachment ReadAudioSidecar(string sidecarPath) =>
      DeserializeAudio(File.ReadAllText(sidecarPath));

   public static ImageAttachment ReadImageSidecar(string sidecarPath) =>
      DeserializeImage(File.ReadAllText(sidecarPath));
}
