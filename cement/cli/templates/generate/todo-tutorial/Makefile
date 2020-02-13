.PHONY: clean develop test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete

develop:
	python3 -m venv env --without-pip
	curl -s -N https://bootstrap.pypa.io/get-pip.py | env/bin/python3
	env/bin/pip3 install -r requirements-dev.txt
	env/bin/pip3 install -e .
	@echo
	@echo "Setup complete. Now run: source env/bin/activate"
	@echo

test:
	python -m pytest \
		-v \
		--cov=todo \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t todo:latest .

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
