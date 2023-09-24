# Extremely slow to load and has a metric ton of dependencies.
#
# import pytest
# import unidic_combo
# import deplacy
#
#
# kindai = unidic_combo.load("kindai")
#
#
# @pytest.mark.parametrize('sentence, expected', [
#     ("探しているんですか", ['探す', 'て', '居る', 'の', 'です', 'か']),  # good: 居る
#     ("としたら", ['と', '為る', 'た']),  # good: 為る
#     ("離れていくよ", ['離れる', 'て', '行く', 'よ']),  # good: 行く
#     ("いつまでも来ないと知らないからね", ['何時', 'まで', 'も', '来る', 'ない', 'と', '知る', 'ない', 'から', 'ね']),  # good: 何時
#     ("ダメダメ私を殺して", ['駄目', '駄目', '私', 'を', '殺す', 'て']),  # good: 駄目
#     ("夢を見た", ['夢', 'を', '見る', 'た']),
#     ("言われるまで気づかなかった", ['言う', 'れる', 'まで', '気付く', 'ない', 'た']),  # good: 気付く
#     ("行きたい所全部行こう", ['行く', 'たい', '所', '全部', '行く']),
#     ("当てられても", ['当てる', 'られる', 'て', 'も']),
#     ("逃げたり", ['逃げる', 'たり']),
#     ("いるのにキス", ['居る', 'の', 'に', 'キス']),  # good: 居る
#     ("するためでした", ['為る', '為', 'です', 'た']),  # good 為る, 為 times two :)
#     ("探しているんですか", ['探す', 'て', '居る', 'の', 'です', 'か']),  # good: 居る
#     ("一度聞いたことがある", ['一', '度', '聞く', 'た', '事', 'が', '有る']),  # good: 有る
#     ("よかった", ['良い', 'た']),  # good: 良い
#     ("良ければ", ['良い', 'ば']),  # good: ば
#     ("良かったら", ['良い', 'た']),  # good
#     ("良くない", ['良い', '無い']),  # good: 無い
#     ("よかったじゃん", ['良い', 'た', 'じゃん']),  # good
#     ("言えばよかった", ['言う', 'ば', '良い', 'た'])  # good: 良い
# ])
# def test_unidic2ud(sentence:str, expected:list[str]) -> None:
#     result1 = kindai(sentence)
#
#     print("")
#     print(sentence)
#     print(deplacy.render(result1,Japanese=True))
#     # print(result1.to_tree())
#     #
#     #
#     # result2 = default(sentence)
#     # print(result2.to_tree())
#     #
#     # result3 = cabocha.parse(sentence)
#     # print(result3)