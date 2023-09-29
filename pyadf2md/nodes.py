import enum
from typing import Dict, Optional, List


class NodeType(enum.Enum):
    PARAGRAPH = (0, 'paragraph')
    TEXT = (1, 'text')
    HARD_BREAK = (2, 'hardBreak')
    BULLET_LIST = (3, 'bulletList')
    LIST_ITEM = (4, 'listItem')
    PANEL = (5, 'panel')

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
    _marks: List

    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)

        if 'text' not in node_dict:
            raise ValueError("text node must contain 'text' attribute")

        self._text = node_dict['text']
        self._marks = node_dict['marks'] if 'marks' in node_dict else list()

    @property
    def text(self) -> str:
        return self._text

    @property
    def marks(self) -> List[str]:
        out = list()
        for m in self._marks:
            if 'type' not in m:
                raise ValueError(f"marks do not contain 'type' attribute")
            out.append(m['type'])

        return out


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


def create_node_from_dict(node_dict: Dict) -> Optional[Node]:
    if 'type' not in node_dict:
        return None

    node_type = NodeType.from_string(node_dict['type'])
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

    raise NotImplementedError(f"unhandled node type '{node_type}'")


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
