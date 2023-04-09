VENV_BASE ?= venv/
PYTHON ?= python3

init: requirements_dev.txt
	if [ "$(VENV_BASE)" ]; then \
		if [ ! -d "$(VENV_BASE)" ]; then \
			$(PYTHON) -m venv $(VENV_BASE); \
			$(VENV_BASE)bin/pip install --upgrade pip; \
			$(VENV_BASE)bin/pip install -r requirements_dev.txt; \
			$(VENV_BASE)bin/pip install -e . ; \
		fi; \
	fi

test:
	pytest tests

build:
	docker build -f DockerfileDebug -t sos-ansible-debug:latest .
	docker build -f Dockerfile -t sos-ansible:latest .

clean:
	rm -rf __pycache__ sos_ansible.egg-info
	rm -rf $(VENV_BASE)
