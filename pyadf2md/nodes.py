import enum
from typing import Dict, Optional, List


class NodeType(enum.Enum):
    PARAGRAPH = (0, 'paragraph')
    TEXT = (1, 'text')
    HARD_BREAK = (2, 'hardBreak')
    BULLET_LIST = (3, 'bulletList')
    LIST_ITEM = (4, 'listItem')
    PANEL = (5, 'panel')
    TABLE = (6, 'table')
    TABLE_ROW = (7, 'tableRow')
    TABLE_HEADER = (8, 'tableHeader')
    TABLE_CELL = (9, 'tableCell')

    def __str__(self):
        return self.value[1]

    @classmethod
    def from_string(cls, s):
        for value in cls:
            if value.value[1] == s:
                return value
        raise ValueError(f"enum '{cls.__name__}' doesn't have value with string '{s}'")

    @classmethod
    def supported_values(cls):
        return [e.value[1] for e in NodeType]


class Node(object):
    _type: NodeType
    _type_str: str
    _attrs: Dict
    _content: List
    _child_nodes: List

    def __init__(self, node_dict: Dict):
        if 'type' not in node_dict:
            raise ValueError("node must contain 'type' attribute")

        self._type_str = node_dict['type']
        self._type = NodeType.from_string(self._type_str)
        self._attrs = node_dict['attrs'] if 'attrs' in node_dict else dict()
        self._content = node_dict['content'] if 'content' in node_dict else list()

        self._child_nodes = list()
        for child_node in self._content:
            self._child_nodes.append(create_node_from_dict(child_node))

    @property
    def type(self) -> NodeType:
        return self._type

    @property
    def child_nodes(self) -> List:
        return self._child_nodes


class ParagraphNode(Node):
    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)


class TextNode(Node):
    _text: str
    _marks: List[Dict]
    _link: Optional[str] = None
    _is_bold: bool = False
    _is_italic: bool = False

    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)

        if 'text' not in node_dict:
            raise ValueError("text node must contain 'text' attribute")

        self._text = node_dict['text']
        self._marks = node_dict['marks'] if 'marks' in node_dict else list()

        for mark in self._marks:
            if 'type' not in mark:
                print(f"WARNING mark does not contain 'type' attribute")
                continue

            mark_type = mark['type']

            if mark_type == 'strong':
                self._is_bold = True

            if mark_type == 'em':
                self._is_italic = True

            if mark_type == 'link':
                if 'attrs' not in mark:
                    print("ERROR link node does not contain 'attrs' attribute")
                    continue

                if 'href' not in mark['attrs']:
                    print("ERROR link's attrs node does not contain 'href' attribute")
                    continue

                self._link = mark['attrs']['href']

    @property
    def text(self) -> str:
        return self._text

    @property
    def link(self) -> Optional[str]:
        return self._link

    @property
    def is_bold(self) -> bool:
        return self._is_bold

    @property
    def is_italic(self) -> bool:
        return self._is_italic


class BulletListNode(Node):
    _elements: List

    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)

        self._elements = list()
        for child_node in self._child_nodes:
            # make sure we have only listItem as children of the node
            if child_node.type != NodeType.LIST_ITEM:
                print(f"WARNING '{NodeType.LIST_ITEM.value}' expected under bulletList; but '{child_node.type}' "
                      f"appeared")
                continue

            self._elements.append(child_node)

    @property
    def elements(self) -> List:
        return self._elements


class ListItemNode(Node):
    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)


class HardBreakNode(Node):
    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)


class PanelNode(Node):
    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)


class TableRow(Node):
    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)

    @property
    def column_count(self) -> int:
        count = 0
        for child in self.child_nodes:
            if child.type in [NodeType.TABLE_HEADER, NodeType.TABLE_CELL]:
                # TODO add support colspan
                count += child.colspan

        return count


class TableNode(Node):
    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)

    @property
    def header(self) -> Optional[TableRow]:
        headers = list(filter(
            lambda node: node.type == NodeType.TABLE_ROW and
                         len(list(filter(
                             lambda child: child.type == NodeType.TABLE_HEADER,
                             node.child_nodes
                         ))) > 0,
            self.child_nodes)
        )

        if len(headers) == 0:
            return None

        if len(headers) > 0:
            print(f'WARNING table contains more than one header')

        return headers[0]


class TableCell(Node):
    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)

    @property
    def colspan(self) -> int:
        return self._attrs['colspan'] if 'colspan' in self._attrs else 1


class TableHeader(TableCell):

    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)


def create_node_from_dict(node_dict: Dict) -> Optional[Node]:
    if 'type' not in node_dict:
        return None

    try:
        node_type = NodeType.from_string(node_dict['type'])
    except ValueError as ex:
        raise NotImplementedError(f"unhandled node type '{node_dict['type']}'")

    if node_type == NodeType.TEXT:
        return TextNode(node_dict)
    elif node_type == NodeType.PARAGRAPH:
        return ParagraphNode(node_dict)
    elif node_type == NodeType.HARD_BREAK:
        return HardBreakNode(node_dict)
    elif node_type == NodeType.BULLET_LIST:
        return BulletListNode(node_dict)
    elif node_type == NodeType.LIST_ITEM:
        return ListItemNode(node_dict)
    elif node_type == NodeType.PANEL:
        return PanelNode(node_dict)
    elif node_type == NodeType.TABLE:
        return TableNode(node_dict)
    elif node_type == NodeType.TABLE_ROW:
        return TableRow(node_dict)
    elif node_type == NodeType.TABLE_HEADER:
        return TableHeader(node_dict)
    elif node_type == NodeType.TABLE_CELL:
        return TableCell(node_dict)

    raise RuntimeError(f"unhandled node type '{node_type}'")


def create_nodes_from_list(node_dict_list: List[Dict]) -> List[Node]:
    out = list()

    idx = 0
    for node_dict in node_dict_list:
        new_node = create_node_from_dict(node_dict)
        if not new_node:
            print(f'WARNING failed to create node from dict (list_index={idx})')
        else:
            out.append(new_node)

        idx += 1

    return out
