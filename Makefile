lint:
	pre-commit run -a --hook-stage manual $(hook)

test:
	pytest

install:
	pip install -e .
	pre-commit install
