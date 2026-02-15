using System;
using System.Collections.Generic;

namespace JAStudio.Core.Tests.Fixtures.BaseData.SampleData;

public class SentenceSpec : IEquatable<SentenceSpec>
{
   public SentenceSpec(string question, string answer)
   {
      Question = question;
      Answer = answer;
   }

   public string Question { get; }
   public string Answer { get; }

   public override string ToString() => $"""SentenceSpec("{Question}", "{Answer}")""";

   public override bool Equals(object? obj) => Equals(obj as SentenceSpec);

   public bool Equals(SentenceSpec? other) =>
      other is not null
   && other.Question == Question
   && other.Answer == Answer;

   public override int GetHashCode() => Question.GetHashCode();

   public static readonly List<SentenceSpec> TestSentenceList =
   [
      new("な何をそんなに一生懸命探しているんですか", "Wh-What are you searching for so desperately?"),
      new("ついに素晴らしい女性に逢えた。", "I was finally able to meet a wonderful woman."),
      new("昨夜恐ろしい夢を見た。", "I had a terrible dream last night.恐ろしい -- terrible, awful"),
      new("一度夢を見た", "Once, [I] had a dream."),
      new("言われるまで気づかなかった", "[I] didn't notice, until [it] was said."),
      new("それなのに先生に当てられてもちゃんと答えられるし", "And yet, when the teacher calls on him, he can answer correctly."),
      new("一度失敗して泣いたり逃げたりすると", "If you fail once, cry, run away, and so on ..."),
      new("私に日記を書くように言ったのも自分が楽をするためでした", "He only told me I should keep a diary to make things easier on himself."),
      new("自分のことを知ってもらえてない人に話しかけたりするのって", "Talking to people who don't know you."),
      new("ううん　俺で良かったらいくらでも付き合うから", "no | if-I-will-do | as-much-as-you-want | accompany | so..."),
      new("そんなに気になるなら あの時俺も友達だって言えばよかったじゃん", "If it bothers you that much, you should have said you were her friend, too."),
      new("話したいことって ひょっとしたら ヨリ戻そうってのかもなあ", "Something she wants to say, huh? It could be that she wants to get back together."),
      new("まあ　でも　それが本当の藤宮なんだとしたら 藤宮にとってお前は特別な存在ってことだよな", "Umm... However, if we assume that that's the real Fujimiya, then you must be special to her, right?"),
      new("だとしたら　今のままでいいんじゃねぇの", "If that's true, then aren't things fine as they are?"),
      new("あいつが話の中に出てくるのが", "But when that guy comes up in our conversation...")
   ];
}
