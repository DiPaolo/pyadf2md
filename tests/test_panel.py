import json

from pyadf2md.adf2md import adf2md


def test_panel(read_input_file):
    input_json_text = read_input_file('data_panel.json')
    json_data = json.loads(input_json_text)

    expected_md_text = read_input_file('data_panel_expected_result.txt')

    md_text = adf2md(json_data)

    assert md_text == expected_md_text
