"""Unit tests for file_handling"""
import os
import os.path
import json
import pytest

from sos_ansible.modules.file_handling import (
    read_policy,
    validate_out_dir,
    create_case_dir,
    create_output,
    process_rule,
    data_input,
    rules_processing,
)

from sos_ansible.modules.config_manager import ConfigParser
from sos_ansible.tests import data


policy_mock = json.loads(
    """{
    "Filesystem": {
        "files": [
            "df"
        ],
        "path": "",
        "query": "100%"
    }
}
"""
)


class TestFileHandling:
    """Testing Instance"""

    def setup_method(self):
        """Creating object"""
        self.data = os.path.abspath(os.path.dirname(data.__file__))

    @pytest.fixture
    def cleanup_fixture(self):
        """My Cleanup Fixture"""
        try:
            os.remove("sos-ansible.log")
        except Exception as error:  # pylint: disable=broad-except
            print(error)

    @pytest.mark.parametrize(
        "file, expected",
        [
            ("rules.json", policy_mock),
            ("empty.json", dict()),
            ("missing.json", dict()),
        ],
    )
    @pytest.mark.usefixtures("cleanup_fixture")
    def test_read_policy(self, file, expected):
        """Testing read_policy Failures"""
        outdata = read_policy(os.path.join(self.data, file))
        assert expected == outdata

    def test_validate_out_dir(self):
        """Testing validate_out_dir Failures"""
        outdata = os.path.join(self.data, "outdata")
        case_out = os.path.join(outdata, "9999999")
        validate_out_dir("9999999", outdata)
        assert not os.path.isdir(case_out)

    def test_validate_out_dir_exist(self):
        """Testing validate_out_dir Failures"""
        outdata = os.path.join(self.data, "outdata")
        case_out = os.path.join(outdata, "9999999")
        os.makedirs(case_out)
        validate_out_dir("9999999", outdata)
        assert not os.path.isdir(case_out)

    def test_create_case_dir(self):
        """Testing create_dir Failures"""
        tgt_dir = os.path.join(self.data, "outdata")
        create_case_dir("9999999", "testnode", tgt_dir)

    def test_create_output(self):
        """Testing create_output Failures"""
        pass

    def test_process_rule(self):
        """Testing process_rule Failures"""
        pass

    def test_rules_processing(self):
        """Testing rules_processing Failures"""
        pass
