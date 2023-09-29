from pyadf2md.nodes import NodeType


def test_enum():
    supported_values = NodeType.supported_values()

    # do not use len() intentionally to know how much items do we
    # support + double check when manually update the value
    assert len(supported_values) == 6
    assert supported_values == ['paragraph', 'text', 'hardBreak', 'bulletList', 'listItem', 'panel']
