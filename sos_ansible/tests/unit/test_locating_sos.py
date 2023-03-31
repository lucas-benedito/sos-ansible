"""Unit tests for locating_sos"""
import os
import os.path
import pytest

from sos_ansible.modules.locating_sos import LocateReports
from sos_ansible.tests import data


class TestLocateReports:
    """Testing Instance"""

    def setup_method(self):
        """Creating object"""
        self.report_data = LocateReports()
        self.data = os.path.abspath(os.path.dirname(data.__file__))

    @pytest.fixture
    def cleanup_fixture(self):
        """My Cleanup Fixture"""
        try:
            os.remove("sos-ansible.log")
        except Exception as error:  # pylint: disable=broad-except
            print(error)

    @pytest.mark.usefixtures("cleanup_fixture")
    def test_locate_reports_not_found(self):
        """Testing Failures"""
        invalid_dir = self.report_data.get_tower_hostname(self.data)
        assert invalid_dir == "NOTFOUND"

    @pytest.mark.usefixtures("cleanup_fixture")
    @pytest.mark.parametrize(
        "sosdir,expected",
        [
            ("000000/sosreport-test-000000", False),
            ("0123456/sosreport-test-123456", True),
        ],
    )
    def test_locate_reports_get_hostname(self, sosdir, expected):
        """Testing function get_tower_hostname"""
        join_dir = os.path.join(self.data, sosdir)
        assert self.report_data.get_tower_hostname(join_dir) == (
            "testnode",
            expected,
        )

    @pytest.mark.usefixtures("cleanup_fixture")
    @pytest.mark.parametrize(
        "sosdir,hostname, expected",
        [("000000", "testnode", False), ("0123456", "testnode", True)],
    )
    def test_locate_outdata(self, sosdir, hostname, expected):
        """Testing function run"""
        outdata = self.report_data.run(self.data, sosdir)
        assert hostname in outdata[0]["hostname"]
        assert outdata[0]["controller"] is expected
