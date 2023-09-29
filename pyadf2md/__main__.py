import json

from pyadf2md.adf2md import adf2md

with open('tests/data/data_paragraph.json', 'r') as f:
    data = json.load(f)
    md_text = adf2md(data)

    print(md_text)

    with open('tests/data/README.md', 'w') as f:
        f.write(md_text)
