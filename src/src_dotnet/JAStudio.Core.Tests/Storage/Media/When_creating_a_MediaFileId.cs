using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Core.Storage.Media;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.Storage.Media;

public class When_creating_a_MediaFileId
{
   public class via_New : When_creating_a_MediaFileId
   {
      readonly MediaFileId _id1 = MediaFileId.New();
      readonly MediaFileId _id2 = MediaFileId.New();

      [XF] public void it_is_not_empty() => _id1.IsEmpty.Must().BeFalse();
      [XF] public void each_id_is_unique() => _id1.Must().NotBe(_id2);
   }

   public class via_Parse : When_creating_a_MediaFileId
   {
      readonly MediaFileId _original = MediaFileId.New();
      readonly MediaFileId _parsed;
      public via_Parse() => _parsed = MediaFileId.Parse(_original.ToString());

      [XF] public void it_roundtrips_through_ToString() => _parsed.Must().Be(_original);
   }

   public class via_TryParse : When_creating_a_MediaFileId
   {
      public class with_a_valid_guid : via_TryParse
      {
         readonly MediaFileId _expected = MediaFileId.New();
         readonly bool _success;
         readonly MediaFileId _parsed;

         public with_a_valid_guid() => _success = MediaFileId.TryParse(_expected.ToString(), out _parsed);

         [XF] public void it_returns_true() => _success.Must().BeTrue();
         [XF] public void the_parsed_id_matches() => _parsed.Must().Be(_expected);
      }

      public class with_invalid_input : via_TryParse
      {
         [XF] public void it_returns_false_for_garbage() => MediaFileId.TryParse("not-a-guid", out _).Must().BeFalse();
         [XF] public void it_returns_false_for_null() => MediaFileId.TryParse(null, out _).Must().BeFalse();
         [XF] public void it_returns_false_for_empty() => MediaFileId.TryParse("", out _).Must().BeFalse();
      }
   }

   public class with_default_value : When_creating_a_MediaFileId
   {
      [XF] public void it_is_empty() => default(MediaFileId).IsEmpty.Must().BeTrue();
   }
}
