"""Unit tests for config_manager"""
import os
import pytest

from sos_ansible.modules.config_manager import ConfigParser
from sos_ansible.tests import testdata


class TestFileHandling:
    """Testing Instance"""

    def setup_method(self):
        """Creating object"""
        self.data = os.path.abspath(os.path.dirname(testdata.__file__))
        self.config = ConfigParser(home_dir=self.data, tgt_file="sos_ansible.ini")

    @pytest.fixture
    def cleanup_fixture(self):
        """My Cleanup Fixture"""
        try:
            print(self.config.config_file)
            os.remove(self.config.config_file)
        except Exception as error:  # pylint: disable=broad-except
            print(error)

    @pytest.mark.usefixtures("cleanup_fixture")
    @pytest.mark.parametrize(
        "expected",
        [("files")],
    )
    def test_set_config(self, expected):
        """Validating configuration generated automatically"""
        self.config.setup()
        with open(self.config.config_file, "r", encoding="utf-8") as file:
            file_data = file.read()
        assert expected in file_data
