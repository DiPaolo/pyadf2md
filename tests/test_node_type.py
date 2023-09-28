from pyadf2md.nodes import NodeType


def test_enum():
    supported_values = NodeType.supported_values()
    assert len(supported_values) == 3
    assert supported_values == ['paragraph', 'text', 'hardBreak']
