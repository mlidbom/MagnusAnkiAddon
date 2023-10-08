from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
from sysutils.ex_str import full_width_space, newline
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_spec import UDTreeSpec

def run_tests(expected: UDTreeSpec, parser: UDTokenizer, sentence: str, depth: int) -> None:
    print()
    parser = parser if parser else ud_parsers.best
    # noinspection PyArgumentEqualDefault
    real_result = ud_tree_builder.build_tree(parser, sentence, collapse_identical_levels_above_level=-1)

    # noinspection PyArgumentEqualDefault
    full_collapsed_real_result = ud_tree_builder.build_tree(parser, sentence, collapse_identical_levels_above_level=-1)
    full_spec_result = UDTreeSpec.from_ud_tree(full_collapsed_real_result, max_depth=98)
    print(f"str full: {sentence}")
    print(str(full_spec_result))

    spec_result = UDTreeSpec.from_ud_tree(real_result, max_depth=depth)

    print(f"""
{parser.name} : {sentence}
{parser.parse(sentence).to_tree()}

str: {sentence}
{str(spec_result)}

expected-repr:
{repr(expected)}

repr:
{repr(spec_result)}

repr-single-line:
{repr(spec_result).replace(newline, '').replace(full_width_space, '')}
""")

    assert spec_result == expected
