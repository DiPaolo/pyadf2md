from typing import List, Optional

from pyadf2md.nodes import Node, NodeType


def gen_md_from_root_node(root_node: Node) -> str:
    try:
        root_node_presenter = create_node_presenter_from_node(root_node, True, False)
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

        idx = 0
        cur_node_type = None
        for child in self._node.child_nodes:
            child_presenter = create_node_presenter_from_node(child, idx == 0, cur_node_type == NodeType.HARD_BREAK,
                                                              self._node)
            if not child_presenter:
                print(f"WARNING failed to create child node presenter for node ({child.type})")
            else:
                self._child_presenters.append(child_presenter)

            idx += 1
            cur_node_type = child.type

    def __str__(self):
        return ''.join([str(child_presenter) for child_presenter in self._child_presenters])

    @property
    def node(self) -> Node:
        return self._node

    @property
    def child_presenters(self) -> List:
        return self._child_presenters


class ParagraphPresenter(NodePresenter):
    _no_leading_newlines: bool

    def __init__(self, node: Node, no_leading_newlines=False):
        super().__init__(node)

        self._no_leading_newlines = no_leading_newlines

    def __str__(self):
        out = ''
        if not self._no_leading_newlines:
            out += '\n'
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
        return '  \n'


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


class PanelPresenter(NodePresenter):
    def __init__(self, node: Node, no_leading_newlines=False):
        super().__init__(node)

    def __str__(self):
        out_lines = list()
        for child_presenter in self._child_presenters:
            cur_presenter_lines = str(child_presenter).splitlines()
            for line in cur_presenter_lines:
                out_lines.append(f'> {line}')

        return '\n'.join(out_lines)


class TablePresenter(NodePresenter):
    def __init__(self, node: Node):
        super().__init__(node)

    def __str__(self):
        out = ''

        header_presenters = list(
            filter(lambda child: len(list(
                filter(lambda child_child: child_child.node.type == NodeType.TABLE_HEADER,
                       child.child_presenters))) > 0,
                   self._child_presenters)
        )

        # if len(header_presenters) > 0:
        #     if len(header_presenters) > 1:
        #         print(f'WARNING table presenter contains more than one header presenter')
        #
        #     header_str = str(header_presenters[0])
        #     out += header_str
        #     out += '-' * len(header_str)

        for row_presenter in self._child_presenters:
            out += f'{str(row_presenter)}'

            is_header = len(list(filter(lambda child_child: child_child.node.type == NodeType.TABLE_HEADER,
                                        row_presenter.child_presenters))) > 0
            if is_header:
                # insert separator like this:
                # | --- | --- | --- |
                col_count = row_presenter.column_count
                out += f"| {' | '.join(['---'] * col_count)} |\n"

        return out


class TableRowPresenter(NodePresenter):
    def __init__(self, node: Node):
        super().__init__(node)

    def __str__(self):
        return f"| {' | '.join([str(child_presenter) for child_presenter in self._child_presenters])} |\n"

    @property
    def column_count(self) -> int:
        return self.node.column_count


class TableHeaderPresenter(NodePresenter):
    def __init__(self, node: Node):
        super().__init__(node)


class TableCellPresenter(NodePresenter):
    def __init__(self, node: Node):
        super().__init__(node)


# TODO bad idea with so many flags; needs to be improved
def create_node_presenter_from_node(node: Node, is_first: bool, is_prev_hard_break: bool,
                                    parent_node: Optional[Node] = None) -> NodePresenter:
    if node.type == NodeType.PARAGRAPH:
        no_leading_newlines = not parent_node or is_first or is_prev_hard_break or bool(
            parent_node and parent_node.type == NodeType.LIST_ITEM)
        return ParagraphPresenter(node, no_leading_newlines)
    elif node.type == NodeType.TEXT:
        return TextPresenter(node)
    elif node.type == NodeType.HARD_BREAK:
        return HardBreakPresenter(node)
    elif node.type == NodeType.BULLET_LIST:
        return BulletListPresenter(node)
    elif node.type == NodeType.LIST_ITEM:
        return ListItemPresenter(node)
    elif node.type == NodeType.PANEL:
        return PanelPresenter(node)
    elif node.type == NodeType.TABLE:
        return TablePresenter(node)
    elif node.type == NodeType.TABLE_ROW:
        return TableRowPresenter(node)
    elif node.type == NodeType.TABLE_HEADER:
        return TableHeaderPresenter(node)
    elif node.type == NodeType.TABLE_CELL:
        return TableCellPresenter(node)

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
