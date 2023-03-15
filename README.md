# sos-ansible

This tool has the purpose of achieving easy sosreport reviewing based on custom rules.

Currently WIP. Feel free to provide feedback.

---
## Setup
To use this tool you must install the python requirements either manually or by use of `make init`.

```
$ python -m venv venv
$ source venv/bin/activate
$ make init
```

---
## sosreport location and rules files
Extract all the sosreport files for evaluation on the same directory as per the example:
```
$ tar xf sosreport-lbenedit-431-node-xxxx-xxx-xxx.tar.xz -C /tmp/test_sosreport/9999999
```

Use the rules file located in this project or create your own. Sharing your rules with your peers is the key for this tools success.
```
$ head rules/rules.json                                                                       
{
    "Filesystem": {
        "files": ["df"],
        "path": "",
        "query": "100%"
    }
}
```

---
## Running the tool and checking the logs [WIP]
Generate your report by running the sos_ansible main.py code providing the sosreport and rules args.
```
$ /tmp/git/sos-ansible
$ python sos_ansible
[?] Choose the sos directory: 999999
 > 999999
   03449015

Validating sosreports at the source directory: /tmp/sosreports
/tmp/sosreports
Validating rules in place: /tmp/rules.json
Processing node lbenedit-431-node.example.com:
Summary
lbenedit-431-node.example.com:
--------
Controller Node: True
--------
Filesystem: 0
Tower Info: 0
Instances Capacity: 0
tower errors: 0
OOM: 0
Antivirus: 0
Installed Packages: 10
Running Processes: 98
Supervisor: 0
Nginx: 0
Receptor: 0
LDAP: 0

Read the matches at /tmp/999999
sos-ansible finished.
```

Currently, the tool logs are located on the current directory, file `sos-ansible.log`.
```
2023-03-15 15:17:10,838 DEBUG Target Directory: /tmp, Case Directory: /tmp/999999
2023-03-15 15:17:10,839 CRITICAL Validating sosreports at the source directory: /tmp/sosreports
2023-03-15 15:17:10,839 ERROR /tmp/sosreports
2023-03-15 15:17:10,841 CRITICAL Validating rules in place: /tmp/rules.json
2023-03-15 15:17:10,841 DEBUG Node data: [{'hostname': 'lbenedit-431-node.example.com', 'path': '/tmp/sosreports/999999/sosreport-lbenedit-431-node-xxxx-xxx-xxx', 'controller': True}]
2023-03-15 15:17:10,842 CRITICAL Processing node lbenedit-431-node.example.com:
2023-03-15 15:17:10,842 INFO Skipping /tmp/sosreports/999999/sosreport-lbenedit-431-node-xxxx-xxx-xxx/sos_commands/tower/awx-manage_--version. Path does not exist.
2023-03-15 15:17:10,843 INFO Skipping /tmp/sosreports/999999/sosreport-lbenedit-431-node-xxxx-xxx-xxx/sos_commands/tower/awx-manage_check_license_--data. Path does not exist.
2023-03-15 15:17:10,843 INFO Skipping /tmp/sosreports/999999/sosreport-lbenedit-431-node-xxxx-xxx-xxx/sos_commands/tower/awx-manage_run_wsbroadcast_--status. Path does not exist.
2023-03-15 15:17:10,843 INFO Skipping /tmp/sosreports/999999/sosreport-lbenedit-431-node-xxxx-xxx-xxx/sos_commands/tower/supervisorctl_status. Path does not exist.
2023-03-15 15:17:10,843 INFO Skipping /tmp/sosreports/999999/sosreport-lbenedit-431-node-xxxx-xxx-xxx/sos_commands/tower/awx-manage_list_instances. Path does not exist.
2023-03-15 15:17:10,844 INFO Skipping /tmp/sosreports/999999/sosreport-lbenedit-431-node-xxxx-xxx-xxx/var/log/tower/management_playbooks.log. Path does not exist.
2023-03-15 15:17:10,844 INFO Skipping /tmp/sosreports/999999/sosreport-lbenedit-431-node-xxxx-xxx-xxx/var/log/tower/tower_system_tracking_migrations.log. Path does not exist.
2023-03-15 15:17:10,864 INFO Populating file /tmp/999999/lbenedit-431-node.example.com/Installed_Packages
2023-03-15 15:17:10,868 INFO Populating file /tmp/999999/lbenedit-431-node.example.com/Running_Processes
2023-03-15 15:17:10,870 CRITICAL Summary
lbenedit-431-node.example.com:
--------
Controller Node: True
--------
Filesystem: 1
Tower Info: 0
Instances Capacity: 0
tower errors: 0
OOM: 0
Antivirus: 0
Installed Packages: 10
Running Processes: 98
Supervisor: 0
Nginx: 0
Receptor: 0
LDAP: 0

2023-03-15 15:17:10,870 CRITICAL Read the matches at /tmp/999999
2023-03-15 15:17:10,870 CRITICAL sos-ansible finished.
```

By default, the tool only offers a summary from all rules processed and you can find the details on the output directory `/tmp/{casenumber}`
```
$ cd /tmp/999999/lbenedit-431-node.example.com
$ ls
Filesystem  Installed_Packages  Running_Processes
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

Currently if you need to debug what is happening inside the container you can comment out the ENTRYPOINT and replace it with CMD

example:

```
ENTRYPOINT ["python", "main.py"]

```

Replace with:

```
CMD ["/bin/bash"]

```

Rebuild the container and then use `podman` or `docker` and replace the command:

```
docker build -t sos-ansible-debug:0.0.1 .

podman run -it --rm -v /tmp/:/tmp/ -v /full/path/to/rules.json:/tmp/rules.json -v /full/path/to/sos-ansible.log:/home/ansible/sos-ansible.log sos-ansible:0.0.1 bash
```
