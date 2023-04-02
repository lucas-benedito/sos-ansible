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
)

from sos_ansible.tests import testdata


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
        self.data = os.path.abspath(os.path.dirname(testdata.__file__))

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
            ("empty.json", {}),
            ("missing.json", {}),
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
        assert os.path.isdir(os.path.join(tgt_dir, "9999999"))
        assert os.path.isdir(os.path.join(tgt_dir, "9999999", "testnode"))

    def test_create_output(self):
        """Testing create_output Failures"""
        input_data = """A test file
        Second content
        """
        create_output(self.data, "fake_rule", input_data)
        assert os.path.isfile(os.path.join(self.data, "fake_rule"))

    def test_process_rule(self):
        """Testing process_rule Failures"""

    def test_rules_processing(self):
        """Testing rules_processing Failures"""
