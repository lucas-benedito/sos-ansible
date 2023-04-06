import pytest
import os
import json
from sos_ansible.modules.file_handling import read_policy


@pytest.fixture
def policy(tmp_path):
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
    with open(test_output, "w+") as f:
        f.write(json.dumps(j))
    return test_output


def test_read_policy(policy):
    output = read_policy(policy)
    assert "LDAP" in output
