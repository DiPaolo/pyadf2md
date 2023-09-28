from typing import List, Optional

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

        for child in self._node.child_nodes:
            child_presenter = create_node_presenter_from_node(child, self._node)
            if not child_presenter:
                print(f"WARNING failed to create child node presenter for node ({child.type})")
                continue

            self._child_presenters.append(child_presenter)


class ParagraphPresenter(NodePresenter):
    _no_trailing_newlines: bool

    def __init__(self, node: Node, no_trailing_newlines=False):
        super().__init__(node)

        self._no_trailing_newlines = no_trailing_newlines

        # for child_node in self._node.child_nodes:
        #     self._child_presenters.append(create_node_presenter_from_node(child_node, self._node))

    def __str__(self):
        out = ''
        if not self._no_trailing_newlines:
            out += '\n\n'
        out += ''.join([str(child_presenter) for child_presenter in self._child_presenters])

        return out


class TextPresenter(NodePresenter):
    # _text_node: TextNode

    def __init__(self, node: Node):
        super().__init__(node)

        # self._text_node = TextNode(self._node)

    def __str__(self):
        out = self._node.text

        marks = self._node.marks
        for m in marks:
            if m == 'strong':
                out = bold(out)
            elif m == 'em':
                out = italic(out)

        return out


class HardBreakPresenter(NodePresenter):
    def __init__(self, node: Node):
        super().__init__(node)

    def __str__(self):
        return '\n'


class BulletListPresenter(NodePresenter):
    def __init__(self, node: Node):
        super().__init__(node)

    def __str__(self):
        bulleted_list = list()
        for child_presenter in self._child_presenters:
            bulleted_list.append(f'+ {str(child_presenter)}')

        return '\n'.join(bulleted_list)


class ListItemPresenter(NodePresenter):
    def __init__(self, node: Node):
        super().__init__(node)

    def __str__(self):
        return ''.join([str(child_presenter) for child_presenter in self._child_presenters])


def create_node_presenter_from_node(node: Node, parent_node: Optional[Node] = None) -> NodePresenter:
    if node.type == NodeType.PARAGRAPH:
        no_trailing_newlines = parent_node and parent_node.type == NodeType.LIST_ITEM
        return ParagraphPresenter(node, no_trailing_newlines)
    elif node.type == NodeType.TEXT:
        return TextPresenter(node)
    elif node.type == NodeType.HARD_BREAK:
        return HardBreakPresenter(node)
    elif node.type == NodeType.BULLET_LIST:
        return BulletListPresenter(node)
    elif node.type == NodeType.LIST_ITEM:
        return ListItemPresenter(node)

    raise NotImplementedError(f"markdown presenter: unhandled node type '{node.type}'")


def header1(text: str) -> str:
    return f'# {text}'


def header2(text: str) -> str:
    return f'## {text}'


def header3(text: str) -> str:
    return f'### {text}'


def bold(text: str) -> str:
    return _apply_formatting(text, '**')


def italic(text: str) -> str:
    return _apply_formatting(text, '*')


def _apply_formatting(text: str, format_symbols: str) -> str:
    text, trailing_spaces_count = remove_trailing_spaces(text)
    return f"{format_symbols}{text}{format_symbols}{' ' * trailing_spaces_count}"


def remove_trailing_spaces(text: str) -> (str, int):
    count = 0
    for ch in reversed(text):
        if ch == ' ':
            count += 1
        else:
            break

    # remove trailing spaces and return that string;
    # str[:0] will clear the string, take it into account by using if ... else
    return text[:-count] if count > 0 else text, count
