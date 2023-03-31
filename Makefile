buildcmd:= podman

init: requirements.txt
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests

build:
	${buildcmd} build -f DockerfileDebug -t sos-ansible-debug:latest .
	${buildcmd} build -f Dockerfile -t sos-ansible:latest .

clean:
	rm -rf __pycache__ sos_ansible.egg-info
