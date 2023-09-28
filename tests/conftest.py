import os.path
import pathlib
from typing import Callable

import pytest


@pytest.fixture(scope="module")
def read_input_file() -> Callable[[str], str]:
    def _read_input_json(base_filename: str) -> str:
        cur_file_path = pathlib.Path(__file__).parent.resolve()
        data_dir = os.path.join(cur_file_path, 'data')
        with open(os.path.join(data_dir, base_filename), 'r') as f:
            return f.read()

    return _read_input_json
