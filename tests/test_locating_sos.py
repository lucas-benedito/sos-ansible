"""Unit tests for locating_sos - currently not working fully"""
import os
import os.path
import pytest

from sos_ansible.modules.locating_sos import LocateReports


def test_locate_reports_not_found(tmp_path):
    """Testing Failures"""
    report_data = LocateReports()
    invalid_dir = report_data.get_tower_hostname(tmp_path)
    assert invalid_dir == "NOTFOUND"


@pytest.mark.usefixtures("create_hostname_files")
@pytest.mark.parametrize(
    "sosdir,expected",
    [
        ("000000/sosreport-test-000000", False),
        ("0123456/sosreport-test-123456", True),
    ],
)
def test_locate_reports_get_hostname(tmp_path, sosdir, expected):
    """Testing function get_tower_hostname"""
    join_dir = os.path.join(tmp_path, sosdir)
    report_data = LocateReports()
    assert report_data.get_tower_hostname(join_dir) == (
        "testnode",
        expected,
    )


@pytest.mark.usefixtures("create_hostname_files")
@pytest.mark.parametrize(
    "sosdir,hostname, expected",
    [("000000", "testnode", False), ("0123456", "testnode", True)],
)
def test_locate_outdata(tmp_path, sosdir, hostname, expected):
    """Testing function run"""
    report_data = LocateReports()
    outdata = report_data.run(tmp_path, sosdir)
    print(outdata)
    assert hostname in outdata[0]["hostname"]
    assert outdata[0]["controller"] is expected
