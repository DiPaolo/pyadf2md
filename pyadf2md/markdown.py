from typing import List

from pyadf2md.nodes import Node, NodeType


def gen_md_from_root_node(root_node: Node) -> str:
    try:
        root_node_presenter = create_node_presenter_from_node(root_node)
    except Exception as ex:
        print(f'ERROR failed to create root node presenter: {ex}')
        return ''

    return str(root_node_presenter)


class NodePresenter(object):
    _node: Node
    _child_presenters: List

    def __init__(self, node: Node):
        self._node = node
        self._child_presenters = list()


class ParagraphPresenter(NodePresenter):
    def __init__(self, node: Node):
        super().__init__(node)

        for child_node in self._node.child_nodes:
            self._child_presenters.append(create_node_presenter_from_node(child_node))

    def __str__(self):
        return '\n\n' + ''.join([str(child_presenter) for child_presenter in self._child_presenters])


class TextPresenter(NodePresenter):
    # _text_node: TextNode

    def __init__(self, node: Node):
        super().__init__(node)

        # self._text_node = TextNode(self._node)

    def __str__(self):
        return self._node.text


class HardBreakPresenter(NodePresenter):
    def __init__(self, node: Node):
        super().__init__(node)

    def __str__(self):
        return '\n'


def create_node_presenter_from_node(node: Node) -> NodePresenter:
    if node.type == NodeType.PARAGRAPH:
        return ParagraphPresenter(node)
    elif node.type == NodeType.TEXT:
        return TextPresenter(node)
    elif node.type == NodeType.HARD_BREAK:
        return HardBreakPresenter(node)


def header1(text: str) -> str:
    return f'# {text}'


def header2(text: str) -> str:
    return f'## {text}'


def header3(text: str) -> str:
    return f'### {text}'


def bold(text: str) -> str:
    return f'**{text}**'
