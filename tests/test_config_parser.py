"""Unit tests for config_manager"""
import pytest

from sos_ansible.modules.config_manager import ConfigParser


@pytest.mark.parametrize(
    "expected",
    [("files")],
)
def test_set_config(tmp_path, expected):
    """Validating configuration generated automatically"""
    config = ConfigParser(home_dir=tmp_path)
    config.setup()
    with open(config.config_file, "r", encoding="utf-8") as file:
        file_data = file.read()
    assert expected in file_data
