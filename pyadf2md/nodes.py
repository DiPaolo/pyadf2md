from typing import Dict, Optional, List


class Node(object):
    _type: str
    _attrs: Dict
    _content: List
    _child_nodes: List

    def __init__(self, node_dict: Dict):
        if 'type' not in node_dict:
            raise ValueError("node must contain 'type' attribute")

        self._type = node_dict['type']
        self._attrs = node_dict['attrs'] if 'attrs' in node_dict else dict()
        self._content = node_dict['content'] if 'content' in node_dict else list()

        self._child_nodes = list()
        for child_node in self._content:
            self._child_nodes.append(create_node_from_dict(child_node))

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

    node_type = node_dict['type']
    if node_type == 'text':
        return TextNode(node_dict)
    elif node_type == 'paragraph':
        return ParagraphNode(node_dict)
    elif node_type == 'hardBreak':
        return HardBreak(node_dict)

    raise ValueError(f"unhandled node type '{node_type}'")
    # return None
