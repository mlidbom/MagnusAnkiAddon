using System;
using System.Text.Json;
using System.Text.Json.Serialization;
using JAStudio.Core.Note;

namespace JAStudio.Core.Storage.Media;

sealed class NoteIdJsonConverter : JsonConverter<NoteId>
{
   public override NoteId Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
   {
      var guid = reader.GetGuid();
      return new NoteId(guid);
   }

   public override void Write(Utf8JsonWriter writer, NoteId value, JsonSerializerOptions options) => writer.WriteStringValue(value.Value);
}

sealed class MediaFileIdJsonConverter : JsonConverter<MediaFileId>
{
   public override MediaFileId Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
   {
      var guid = reader.GetGuid();
      return new MediaFileId(guid);
   }

   public override void Write(Utf8JsonWriter writer, MediaFileId value, JsonSerializerOptions options) => writer.WriteStringValue(value.Value);
}

sealed class SourceTagJsonConverter : JsonConverter<SourceTag>
{
   public override SourceTag Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options) => SourceTag.Parse(reader.GetString()!);

   public override void Write(Utf8JsonWriter writer, SourceTag value, JsonSerializerOptions options) => writer.WriteStringValue(value.ToString());
}
