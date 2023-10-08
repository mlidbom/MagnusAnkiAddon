from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
from language_services.universal_dependencies.shared.tree_building.ud_tree import UDTree
from sysutils.ex_str import full_width_space, newline
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_spec import UDTreeSpec

def run_tests_for_level(expected: UDTreeSpec, parser: UDTokenizer, sentence: str, depth: int) -> None:
    print()
    parser = parser if parser else ud_parsers.best
    real_result = ud_tree_builder.build_tree(parser, sentence)
    full_collapsed_real_result = ud_tree_builder.build_tree(parser, sentence)

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

    if depth not in set(node.depth for node in real_result.flatten()):
        raise Exception(f"There are no nodes at depth {depth} in the result set. Please use assert_no_nodes_at_level instead")


    assert spec_result == expected

def assert_no_nodes_at_level(parser: UDTokenizer, sentence: str, depth: int) -> None:
    real_result = ud_tree_builder.build_tree(parser, sentence)
    spec_result = UDTreeSpec.from_ud_tree(real_result, max_depth=98)

    print(f"""
{parser.name} : {sentence}
{parser.parse(sentence).to_tree()}

str: {sentence}
{str(spec_result)}

repr:
{repr(spec_result)}

repr-single-line:
{repr(spec_result).replace(newline, '').replace(full_width_space, '')}
    """)

    if depth in set(node.depth for node in real_result.flatten()):
        raise Exception(f"Nodes were found at depth {depth} in the result set. Please use run_tests_for_level instead")

