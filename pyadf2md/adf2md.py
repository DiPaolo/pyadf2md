from typing import Dict, List

import pyadf2md.nodes as nodes
from pyadf2md import markdown


def adf2md(json_data: Dict | List[Dict]) -> str:
    root_nodes = list()

    if isinstance(json_data, List):
        root_nodes = nodes.create_nodes_from_list(json_data)
    elif isinstance(json_data, Dict):
        root_node = nodes.create_node_from_dict(json_data)
        if root_node:
            root_nodes.append(root_node)

    md_text_list = list()
    for node in root_nodes:
        md_text_list.append(markdown.gen_md_from_root_node(node))

    if len(md_text_list) == 0:
        print(f'WARNING no ADF nodes found')
        return ''

    md_text = '\n\n'.join(md_text_list)
    return md_text
