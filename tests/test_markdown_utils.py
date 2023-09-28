import pytest

from pyadf2md.markdown import remove_trailing_spaces


@pytest.mark.parametrize('text,expected_result_str,expected_count', [
    ('test', 'test', 0),
    ('test1 ', 'test1', 1),
    ('test2  ', 'test2', 2),
    ('test3   ', 'test3', 3),

    (' test4', ' test4', 0),
    ('  test5', '  test5', 0),
    ('   test6', '   test6', 0),

    (' test1 ', ' test1', 1),
    ('  test2  ', '  test2', 2),
    ('   test3   ', '   test3', 3),

    ('', '', 0),
    (' ', '', 1),
    ('  ', '', 2),
    ('   ', '', 3),
])
def test_remove_trailing_spaces(text, expected_result_str, expected_count):
    result_str, count = remove_trailing_spaces(text)

    assert result_str == expected_result_str
    assert count == expected_count
