from pyadf2md.adf2md import nodes


def gen_md_from_root_node(root_node: nodes.Node) -> str:
    return str(root_node)


def header1(text: str) -> str:
    return f'# {text}'


def header2(text: str) -> str:
    return f'## {text}'


def header3(text: str) -> str:
    return f'### {text}'


def bold(text: str) -> str:
    return f'**{text}**'
