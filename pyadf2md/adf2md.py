from typing import Dict

import pyadf2md.nodes as nodes
from pyadf2md import markdown


def adf2md(json_data: Dict) -> str:
    # json_data = json.loads(json_data)

    root_node = nodes.create_node_from_dict(json_data)
    if not root_node:
        return ''

    md_text = markdown.gen_md_from_root_node(root_node)

    with open('tests/data/README.md', 'w') as f:
        f.write(md_text)

    return md_text
