.PHONY: format-code
format-code:
	@black src

.PHONY: test
test:
	@coverage run -m pytest

.PHONY: test-with-coverage
test-with-coverage:
	@coverage run -m pytest
	@coverage report

.PHONY: type-check
type-check:
	@mypy src