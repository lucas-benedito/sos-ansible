init: requirements.txt
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest tests

build:
	docker build -f DockerfileDebug -t quay.io/lucas_benedito/sos-ansible-debug:latest .
	docker build -f Dockerfile -t quay.io/lucas_benedito/sos-ansible:latest .

clean:
	rm -rf __pycache__