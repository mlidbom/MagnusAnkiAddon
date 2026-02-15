namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing;

// Base class for split tokens
public abstract class SplitTokenBase : IAnalysisToken
{
   JNToken Source { get; }
   readonly string _surface;
   readonly string _baseForm;

   protected SplitTokenBase(JNToken source, string surface, string baseForm)
   {
      Source = source;
      _surface = surface;
      _baseForm = baseForm;
   }

   public override JNToken SourceToken => Source;
   public override string Surface => _surface;
   public override string BaseForm => _baseForm;

   public override string ToString() => $"{GetType().Name}('{Surface}', '{BaseForm}')";
}

// Base class for dictionary form tokens
public abstract class DictionaryFormsTokenBase : SplitTokenBase
{
   protected DictionaryFormsTokenBase(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}

   // TODO: this feels odd, but without it it seems that things go haywire...
   public override bool IsInflectableWord => true;
}

// Dictionary form stem
public class DictionaryFormStem : DictionaryFormsTokenBase
{
   public DictionaryFormStem(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}

   public override bool IsDictionaryVerbFormStem => true;
}

// Dictionary form inflection
public class DictionaryFormInflection : DictionaryFormsTokenBase
{
   public DictionaryFormInflection(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}

   public override bool IsDictionaryVerbInflection => true;
}

// Godan dictionary form stem
public class GodanDictionaryFormStem : DictionaryFormStem
{
   public GodanDictionaryFormStem(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}
}

// Godan potential dictionary form stem
public class GodanPotentialDictionaryFormStem : GodanDictionaryFormStem
{
   public GodanPotentialDictionaryFormStem(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}

   public override bool IsGodanPotentialStem => true;

   // TODO: this leaves us with these tokens claiming both to be an ichidan (via the base class) and a godan... We can't tell which, but still..
   public override bool IsGodanVerb => true;
}

// Godan dictionary form inflection
public class GodanDictionaryFormInflection : DictionaryFormInflection
{
   public GodanDictionaryFormInflection(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}
}

// Godan potential inflection dictionary form stem
public class GodanPotentialInflectionDictionaryFormStem : DictionaryFormStem
{
   public GodanPotentialInflectionDictionaryFormStem(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}

   public override bool IsGodanPotentialInflection => true;
}

// Godan potential inflection dictionary form inflection
public class GodanPotentialInflectionDictionaryFormInflection : DictionaryFormInflection
{
   public GodanPotentialInflectionDictionaryFormInflection(JNToken source)
      : base(source, "る", "る") {}
}

// Ichidan dictionary form stem
public class IchidanDictionaryFormStem : DictionaryFormStem
{
   public IchidanDictionaryFormStem(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}
}

// Ichidan dictionary form inflection
public class IchidanDictionaryFormInflection : DictionaryFormInflection
{
   public IchidanDictionaryFormInflection(JNToken source)
      : base(source, "る", "る") {}
}

// Kuru verb dictionary form stem
public class KuruVerbDictionaryFormStem : DictionaryFormStem
{
   public KuruVerbDictionaryFormStem(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}
}

// Kuru verb dictionary form inflection
public class KuruVerbDictionaryFormInflection : DictionaryFormInflection
{
   public KuruVerbDictionaryFormInflection(JNToken source)
      : base(source, "る", "る") {}
}

// Suru verb dictionary form stem
public class SuruVerbDictionaryFormStem : DictionaryFormStem
{
   public SuruVerbDictionaryFormStem(JNToken source, string surface, string baseForm)
      : base(source, surface, baseForm) {}
}

// Suru verb dictionary form inflection
public class SuruVerbDictionaryFormInflection : DictionaryFormInflection
{
   public SuruVerbDictionaryFormInflection(JNToken source)
      : base(source, "る", "る") {}
}
