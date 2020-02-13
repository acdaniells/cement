.PHONY: develop test format docs clean dist

help:
	@echo "usage: make <rule>"
	@echo
	@echo "Cement Makefile containing useful rules for developers."
	@echo
	@echo "rules:"
	@echo "  clean          clean the package"
	@echo "  develop        install development version"
	@echo "  test           run the full test suite"
	@echo "  test-core      run the core test suite"
	@echo "  comply         run code quality checks"
	@echo "  format         run code formatting"
	@echo "  docs           build documentation"
	@echo "  dist           build distribution"

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

	rm -f set_proxy.sh
	rm -rf .coverage*/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf docs/build/
	rm -rf *.egg-info/

develop:
	python3 -m venv env --without-pip
	curl -s -N https://bootstrap.pypa.io/get-pip.py | env/bin/python3
	env/bin/pip3 install -r requirements-dev.txt
	env/bin/pip3 install -e .
	@echo
	@echo "Setup complete. Now run: source env/bin/activate"
	@echo

test:
	env/bin/python3 -m pytest -v --cov=cement --cov-report=term --cov-report=html:coverage tests/

test-core:
	env/bin/python3 -m pytest -v --cov=cement.core --cov-report=term --cov-report=html:coverage tests/core

comply:
	flake8 cement/ tests/

format:
	isort --recursive .
	black --exclude cement/cli/templates/generate cement/ tests/

docs:
	env/bin/python3 setup.py build_sphinx
	@echo
	@echo DOC: "file://"$$(echo `pwd`/docs/build/html/index.html)
	@echo

dist: clean
	env/bin/python3 setup.py sdist bdist_wheel
