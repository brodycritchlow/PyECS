.PHONY: docs-build docs-clean docs-serve docs-install

docs-install:
	uv pip install -e ".[docs]"

docs-build:
	cd docs/sphinx && make html

docs-clean:
	cd docs/sphinx && make clean

docs-serve:
	cd docs/sphinx && python -m http.server -d _build/html 8000