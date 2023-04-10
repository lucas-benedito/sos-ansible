"""place new fixtures here"""
import os
import json
import tarfile
import pytest


@pytest.fixture(name="policy")
def policy_fixture(tmp_path):
    """dummy policy"""
    j = {
        "Tower": {"files": ["fower.log"], "path": "var/log/tower", "query": "error"},
        "Receptor": {
            "files": ["receptor.log", "receptor.error"],
            "path": "var/log/receptor",
            "query": "error",
        },
        "Nginx": {
            "files": ["nginx.log", "nginx.error"],
            "path": "var/log/nginx",
            "query": "error",
        },
        "Supervisor": {
            "files": ["supervisor.log", "awx-dispatcher.log", "awx-uwsgi.log"],
            "path": "var/log/supervisor",
            "query": "traceback",
        },
        "Dispatcher": {
            "files": ["dispatcher.log"],
            "path": "var/log/tower",
            "query": "error",
        },
        "LDAP": {
            "files": ["tower.log"],
            "path": "var/log/tower",
            "query": "django_ldap_auth",
        },
    }
    test_output = os.path.join(tmp_path, "rules.json")
    with open(test_output, "w+", encoding="utf-8") as file_out:
        file_out.write(json.dumps(j))
    return test_output


@pytest.fixture(name="bad_json")
def bad_json_fixture(tmp_path):
    """bad json policy"""
    test_output = os.path.join(tmp_path, "rules.json")
    with open(test_output, "w+", encoding="utf-8") as file_out:
        file_out.write('{"foo": "bar",}')
    return test_output


@pytest.fixture(name="directory")
def directory_fixture(tmp_path):
    """test dir with case id"""
    new_dir = os.path.join(tmp_path, "999999")
    return new_dir


@pytest.fixture(name="hostname")
def hostname_fixture():
    """returns a hostname"""
    return "example.com"


@pytest.fixture(name="tar")
def tarball_fixture():
    """create test tar"""
    tar = tarfile.open("test.tar.gz", "w")  # pylint: disable=consider-using-with
    for file in ("tower.log", "dispatcher.log", "task_system.log"):
        with open(file, "w", encoding="utf-8") as new_file:
            new_file.write("ERROR")
        tar.add(file)
    tar.close()
    return tar
