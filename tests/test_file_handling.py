"""file handling test cases"""
import os
import pytest
from sos_ansible.modules.file_handling import (
    read_policy,
    create_case_dir,
    validate_out_dir,
    expand_sosreport,
    create_output,
    data_input,
    rules_processing,
)


def test_read_policy(policy):
    """test good json read policy"""
    output = read_policy(policy)
    assert "LDAP" in output


def test_bad_json_read_policy(bad_json):
    """tests bad json error handling"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read_policy(bad_json)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_missing_json_read_policy(missing_json):
    """tests missing json error handling"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read_policy(missing_json)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_create_case_dir(tmp_path, hostname):
    """tests create function"""
    newdir = create_case_dir("999999", hostname, tmp_path)
    assert os.path.exists(newdir)


def test_create_case_dir_failure(tmp_path, hostname):
    """tests failure create case dir function"""
    final_dir = os.path.join(tmp_path, "test")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        create_case_dir("999999", hostname, final_dir)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_expand_tar(tar, tmp_path):
    """test expanding sosreport"""
    expand_sosreport([tar.name], "999999", tmp_path)
    final_dir = os.path.join(tmp_path, "999999")
    expanded = os.listdir(final_dir)
    assert "tower.log" in expanded


def test_validate_out_dir(tmp_path):
    """test validate_out function"""
    assert os.path.isdir(tmp_path)
    final_dir = os.path.join(tmp_path, "999999")
    validate_out_dir("999999", tmp_path)
    assert not os.path.isdir(final_dir)
    os.mkdir(final_dir)
    validate_out_dir("999999", tmp_path)
    assert not os.path.isdir(final_dir)


def test_create_output(tmp_path):
    """test create_output function"""
    assert os.path.isdir(tmp_path)
    test_data = "Data to write"
    create_output(tmp_path, "Filesystem", test_data)
    expanded = os.listdir(tmp_path)
    assert "Filesystem" in expanded


@pytest.mark.usefixtures("create_hostname_files")
@pytest.mark.parametrize(
    "sosdir,name,expected",
    [
        ("000000", "testnode", "LDAP"),
    ],
)
def test_data_input(tmp_path, policy, sosdir, name, expected):
    """test data_input function"""
    node_data, curr_policy = data_input(tmp_path, policy, sosdir)
    assert name in node_data[0]["hostname"]
    assert expected in curr_policy


@pytest.mark.usefixtures("create_hostname_files")
@pytest.mark.parametrize(
    "sosdir",
    [
        ("0123456"),
    ],
)
def test_rules_processing(tmp_path, policy, sosdir):
    """test rules processing function"""
    node_data, curr_policy = data_input(tmp_path, policy, sosdir)
    rules_processing(node_data, curr_policy, sosdir, "debug", tmp_path)
