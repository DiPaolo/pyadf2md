import json
import pprint

from pyadf2md.adf2md import adf2md

with open('tests/data/data_bullet_list.json', 'r') as f:
    data = json.load(f)
    md_text = adf2md(data)
    print(md_text)
