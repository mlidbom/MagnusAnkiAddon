from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
from sysutils.ex_str import full_width_space
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_spec import UDTreeSpec

def run_tests(expected: UDTreeSpec, parser: UDTokenizer, sentence: str, depth:int) -> None:
    print()
    parser = parser if parser else ud_parsers.best
    real_result = ud_tree_builder.build_tree(parser, sentence, collapse_identical_levels_above_level=99)

    # noinspection PyArgumentEqualDefault
    full_collapsed_real_result = ud_tree_builder.build_tree(parser, sentence, collapse_identical_levels_above_level=depth)
    full_spec_result = UDTreeSpec.from_ud_tree(full_collapsed_real_result, max_depth=98)
    print(f"str full: {sentence}")
    print(str(full_spec_result))

    spec_result = UDTreeSpec.from_ud_tree(real_result, max_depth=depth)
    print(f"{parser.name} : {sentence}")
    print(parser.parse(sentence).to_tree())
    print()
    print(f"str: {sentence}")
    print(str(spec_result))
    print("expected-repr:")
    print(repr(expected))
    print("repr:")
    print(repr(spec_result))
    print("repr-single-line:")
    print(repr(spec_result).replace("\n", '').replace(full_width_space, ''))

    assert spec_result == expected