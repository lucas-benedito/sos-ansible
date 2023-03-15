init: requirements.txt
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests

clean:
	rm -rf __pycache__