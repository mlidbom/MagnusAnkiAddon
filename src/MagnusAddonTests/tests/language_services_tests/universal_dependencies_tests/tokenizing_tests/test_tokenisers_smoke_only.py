from fixtures.base_data.sample_data import sentence_spec
from language_services.universal_dependencies import ud_tokenizers

def test_smoke_test_representative_tokenizers() -> None:
    for tokenizer in ud_tokenizers.representative_tokenizers:
        for sentence in sentence_spec.test_sentence_list:
            print(tokenizer.name)
            tokenized = tokenizer.tokenize(sentence.question)
            print(tokenized)

            print(f"""
tree:
{tokenized.to_tree()}
""")