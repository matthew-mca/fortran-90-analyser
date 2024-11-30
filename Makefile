SRC_ROOT="src/python"

.PHONY: format-code
format-code:
	@ruff format $(SRC_ROOT)

.PHONY: dependencies
dependencies:
	@uv pip sync requirements.txt requirements-dev.txt

.PHONY: lint
lint:
	@ruff check $(SRC_ROOT)

.PHONY: test
test:
	@coverage run -m pytest

.PHONY: test-integration
test-integration:
	@coverage run -m pytest src/python/tests/integration

.PHONY: test-unit
test-unit:
	@coverage run -m pytest src/python/tests/unit

.PHONY: test-with-coverage
test-with-coverage:
	@coverage run -m pytest
	@coverage report

.PHONY: type-check
type-check:
	@mypy $(SRC_ROOT)

.PHONY: sort-imports
sort-imports:
	@ruff check --select I --fix $(SRC_ROOT)