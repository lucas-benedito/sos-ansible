[![GPL-3.0 license](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](https://github.com/lucas-benedito/sos-ansible/blob/devel/LICENSE)[![PyPI version](https://img.shields.io/pypi/v/sos_ansible.svg)](https://pypi.org/project/sos-ansible/)[![PR - Pylint Status](https://github.com/lucas-benedito/sos-ansible/actions/workflows/pylint.yml/badge.svg)](https://github.com/lucas-benedito/sos-ansible/actions/workflows/pylint.yml)[![Python Builds](https://github.com/lucas-benedito/sos-ansible/actions/workflows/python-publish.yml/badge.svg)](https://github.com/lucas-benedito/sos-ansible/actions/workflows/python-publish.yml)

# sos-ansible

This tool has the purpose of achieving easy sosreport reviewing based on custom rules.

---

* [Installation](#installation)
* [Sosreport location and rules files](#sosreport-location-and-rules-files)
* [Running the tool and checking the logs [WIP]](#running-the-tool-and-checking-the-logs-[wip])
* [Running tool via container](#running-tool-via-container)
* [Additional notes for troubleshooting containerized tool](#additional-notes-for-troubleshooting-containerized-tool)
* [Setup Development Environment](#setup-development-environment)
---
## Installation
This tool can be installed from pip
```
$ pip install sos_ansible
```

---
## Sosreport location and rules files
Extract all the sosreport files for evaluation on the same directory as per the example:
```
$ tar xf sosreport-lbenedit-test-node-xxxx-xxx-xxx.tar.xz -C /tmp/test_sosreport/9999999
```

Use the rules file located in this project or create your own. Sharing your rules with your peers is the key for this tools success.
```
$ head rules/rules.json                                                                       
{
    "Filesystem": {
        "files": ["df"],
        "path": "",
        "query": "100%"
    },
    "Installed Packages": {
        "files": [
            "installed-rpms"
        ],
        "path": "",
        "query": "ansible, automation, receptor, hub, keycloak"
    }
}
```

---
## Running the tool and checking the logs
Generate your report by running the sos_ansible main.py code providing the sosreport and rules args.
```
$ /tmp/git/sos-ansible
$ python sos_ansible
[?] Choose the sos directory: 999999
 > 999999
   01234567

Validating sosreports at the source directory: /tmp/sosreports
Validating rules in place: /tmp/rules.json
Processing node lbenedit-test-node.example.com:
Summary:

lbenedit-test-node.example.com:
--------
Controller Node: True
--------
Filesystem: 1
Installed Packages: 10

Read the matches at /tmp/999999
SOS_ANSIBLE - END
```

Currently, the tool logs are located on the current directory, file `sos-ansible.log`.
```
2023-03-15 15:17:10,839 CRITICAL Validating sosreports at the source directory: /tmp/sosreports
2023-03-15 15:17:10,839 ERROR /tmp/sosreports
2023-03-15 15:17:10,841 CRITICAL Validating rules in place: /tmp/rules.json
2023-03-15 15:17:10,841 DEBUG Node data: [{'hostname': 'lbenedit-test-node.example.com', 'path': '/tmp/sosreports/999999/sosreport-lbenedit-test-node-xxxx-xxx-xxx', 'controller': True}]
2023-03-15 15:17:10,841 DEBUG Current policy: {'Filesystem': {'files': ['df'], 'path': '', 'query': '100%'}, 'Installed Packages': {'files': ['installed-rpms'], 'path': '', 'query': 'ansible, automation, receptor, hub, keycloak'},}
DEBUG Target Directory: /tmp, Case Directory: /tmp/999999
2023-03-15 15:17:10,842 CRITICAL Processing node lbenedit-test-node.example.com:
2023-03-15 15:17:10,864 INFO Populating file /tmp/999999/lbenedit-test-node.example.com/Filesystem
2023-03-15 15:17:10,868 INFO Populating file /tmp/999999/lbenedit-test-node.example.com/Installed_Packages
2023-03-15 15:17:10,870 CRITICAL Summary:

lbenedit-test-node.example.com:
--------
Controller Node: True
--------
Filesystem: 1
Installed Packages: 10

2023-03-15 15:17:10,870 CRITICAL Read the matches at /tmp/999999
2023-03-15 15:17:10,870 CRITICAL SOS_ANSIBLE - END
```

By default, the tool only offers a summary from all rules processed and you can find the details on the output directory `/tmp/{casenumber}`
```
$ cd /tmp/999999/lbenedit-test-node.example.com
$ ls
Filesystem  Installed_Packages
$ cat Filesystem
/dev/mapper/rhel-amazing  12345   12345         0 100% /amazingfs
```

## Running tool via container

An alternative to running this on cli directly is to use the container version:

Running the app with docker-compose
```
docker-compose run backend bash
```

Using prebuilt images:
Interactive image:
```
docker pull quay.io/lucas_benedito/sos-ansible-debug
```
App image:
```
docker pull quay.io/lucas_benedito/sos-ansible
```

You may build locally using the following:

from the sos-ansible directory
```
docker build -t sos-ansible:0.0.1 .
``` 


Once the image is built use either `podman` or `docker` to run the command:

``` 
podman run -it --rm -v /tmp/:/tmp/ -v /full/path/to/rules.json:/tmp/rules.json -v /full/path/to/sos-ansible.log:/home/ansible/sos-ansible.log sos-ansible:0.0.1 -d /tmp/sos_reports/ -r /tmp/rules.json -c 999999 
```

Breakdown of args:
  - -d directory where sosreports were untarred(should be /tmp/sos_reports if following the earlier instructions)
  - -r path to rules(this can be whatever you specified in the -v option for mounting)
  - -c case/ticket number where you untarred the sosreport to (example from doc is 999999) this argument is mandatory for containerized invocations


## Additional notes for troubleshooting containerized tool

Currently if you need to debug what is happening inside the container you can use --entrypoint /bin/bash

example:
```
podman run --entrypoint /bin/bash -it --rm -v /tmp/:/tmp/ -v /full/path/to/rules.json:/tmp/rules.json -v /full/path/to/sos-ansible.log:/home/ansible/sos-ansible.log sos-ansible:0.0.1
```

---
## Setup Development Environment
Create virtual environment and use `make init`.
```
$ python -m venv venv
$ source venv/bin/activate
$ make init
```