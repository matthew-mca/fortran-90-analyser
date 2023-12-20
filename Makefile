.PHONY: format-code
format-code:
	@black src/python/

.PHONY: dependencies
dependencies:
	@pip-sync requirements.txt requirements-dev.txt

.PHONY: lint
lint:
	@flake8 src/python/

.PHONY: test
test:
	@coverage run -m pytest

.PHONY: test-with-coverage
test-with-coverage:
	@coverage run -m pytest
	@coverage report

.PHONY: type-check
type-check:
	@mypy src/python/