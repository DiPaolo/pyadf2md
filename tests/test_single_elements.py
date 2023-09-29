import json

import pytest

from pyadf2md.adf2md import adf2md


@pytest.mark.parametrize('element_name', [
    'bold_italic',
    'bullet_list',
    'panel',
    'paragraph',
    'table',
    'table_colspan',
    'link'
])
def test_bullet_list(read_input_file, element_name):
    input_json_text = read_input_file(f'data_{element_name}.json')
    json_data = json.loads(input_json_text)

    expected_md_text = read_input_file(f'data_{element_name}_expected.md')

    md_text = adf2md(json_data)

    assert md_text == expected_md_text
