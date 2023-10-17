from language_services.universal_dependencies import ud_tokenizers
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode
from sysutils.ex_str import full_width_space, newline
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_spec import UDTreeSpec

def run_tests_for_level(expected: UDTreeSpec, parser: UDTokenizer, sentence: str, depth: int) -> None:
    print()
    parser = parser if parser else ud_tokenizers.default
    real_result = ud_tree_builder.build_tree(parser, sentence)

    full_spec_result = UDTreeSpec.from_ud_tree(real_result, max_depth=98)

    found_depths: set[int] = set()

    def register_depths(node: UDTreeNode) -> None:
        found_depths.add(node.depth)

    spec_result = UDTreeSpec.from_ud_tree(real_result, max_depth=depth)

    real_result.visit(register_depths)

    if depth not in found_depths:
        spec_result = UDTreeSpec()

    print(f"""
str full: {sentence}
{str(full_spec_result)}
""")

    print(f"""
{parser.name} : {sentence}
{parser.tokenize(sentence).to_tree()}
""")

    print(f"""
str: {sentence}
{str(spec_result)}
""")

    print(f"""
expected-repr:
{repr(expected)}
""")

    print(f"""
repr:
{repr(spec_result)}
""")

    print(f"""
repr-single-line:
{repr(spec_result).replace(newline, '').replace(full_width_space, '')}
""")

    assert spec_result == expected
