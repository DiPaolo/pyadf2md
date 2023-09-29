import json

from pyadf2md.adf2md import adf2md


def test_paragraph(read_input_file):
    input_json_text = read_input_file('data_paragraph.json')
    json_data = json.loads(input_json_text)

    expected_md_text = read_input_file('data_paragraph_expected_result.txt')

    md_text = adf2md(json_data)

    assert md_text == expected_md_text
