"""file handling test cases"""
import os
import tarfile
import pytest
from sos_ansible.modules.file_handling import read_policy, create_dir, validate_out_dir, expand_sosreport


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


def test_create_dir(directory, hostname):
    """tests create function"""
    newdir = create_dir(directory, hostname)
    assert os.path.exists(newdir)


def test_expand_tar(directory):
    """test expanding sosreport"""
    tar = tarfile.open("test.tar.gz", "w") # pylint: disable=consider-using-with
    for file in ("tower.log", "dispatcher.log", "task_system.log"):
        with open(file, "w", encoding='utf-8') as new_file:
            new_file.write("ERROR")
        tar.add(file)
    tar.close()
    expand_sosreport([tar.name], directory)
    expanded = os.listdir(directory)
    assert "tower.log" in expanded

def test_validate_out_dir(tmp_path):
    """ test validate_out function"""
    assert os.path.isdir(tmp_path)
    validate_out_dir(tmp_path)
    assert not os.path.isdir(tmp_path)
