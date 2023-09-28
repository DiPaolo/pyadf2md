import enum
from typing import Dict, Optional, List


class NodeType(enum.Enum):
    PARAGRAPH = (0, 'paragraph')
    TEXT = (1, 'text')
    HARD_BREAK = (2, 'hardBreak')

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

    def __str__(self):
        return '\n\n' + ''.join([str(node) if node else ' ' for node in self.child_nodes])


class TextNode(Node):
    _text: str
    _marks: List

    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)

        if 'text' not in node_dict:
            raise ValueError("text node must contain 'text' attribute")

        self._text = node_dict['text']
        self._content = node_dict['marks'] if 'marks' in node_dict else list()

    def __str__(self):
        return self._text


class HardBreak(Node):
    def __init__(self, node_dict: Dict):
        super().__init__(node_dict)

    def __str__(self):
        return '\n'


def create_node_from_dict(node_dict: Dict) -> Optional[Node]:
    if 'type' not in node_dict:
        return None

    node_type = NodeType.from_string(node_dict['type'])
    if node_type == NodeType.TEXT:
        return TextNode(node_dict)
    elif node_type == NodeType.PARAGRAPH:
        return ParagraphNode(node_dict)
    elif node_type == NodeType.HARD_BREAK:
        return HardBreak(node_dict)

    raise ValueError(f"unhandled node type '{node_type}'")
    # return None
