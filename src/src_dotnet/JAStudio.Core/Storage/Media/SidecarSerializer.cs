using System;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace JAStudio.Core.Storage.Media;

public static class SidecarSerializer
{
   static readonly JsonSerializerOptions Options = new()
                                                   {
                                                      WriteIndented = true,
                                                      PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                                                      DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingDefault,
                                                      Converters =
                                                      {
                                                         new JsonStringEnumConverter(JsonNamingPolicy.CamelCase),
                                                         new NoteIdJsonConverter(),
                                                         new MediaFileIdJsonConverter()
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

   public static string GetAudioSidecarExtension() => ".audio.json";
   public static string GetImageSidecarExtension() => ".image.json";

   public static string BuildAudioSidecarPath(string mediaFilePath)
   {
      var dir = Path.GetDirectoryName(mediaFilePath) ?? string.Empty;
      var id = Path.GetFileNameWithoutExtension(mediaFilePath);
      return Path.Combine(dir, $"{id}{GetAudioSidecarExtension()}");
   }

   public static string BuildImageSidecarPath(string mediaFilePath)
   {
      var dir = Path.GetDirectoryName(mediaFilePath) ?? string.Empty;
      var id = Path.GetFileNameWithoutExtension(mediaFilePath);
      return Path.Combine(dir, $"{id}{GetImageSidecarExtension()}");
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
