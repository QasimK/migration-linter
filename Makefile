MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
SHELL := bash
.SHELLFLAGS := -euo pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:

COLOR_BLUE = \033[0;94m
COLOR_GREEN = \033[0;32m
NO_COLOR   = \033[m


##     help:    This.
.PHONY: help
help: Makefile
#   Find all double comments and treat them as docstrings
	@echo "make <command>"
	@sed -n 's/^##//p' $<


##     fix: Automatically fix checks (where possible).
.PHONY: fix
fix:
	@echo -e "${COLOR_BLUE}=== isort ===\n${NO_COLOR}"
	@poetry run isort --quiet migration_linter tests

	@echo -e "${COLOR_BLUE}\n=== Black ===\n${NO_COLOR}"
	@poetry run black --quiet migration_linter tests


##     check:   Run basic checks.
.PHONY: check
check:
	@echo -e "${COLOR_BLUE}=== Correctness: Poetry ===\n${NO_COLOR}"
	@poetry --quiet check

	@echo -e "${COLOR_BLUE}\n=== Correctness: Pyflakes ===\n${NO_COLOR}"
	@poetry run pyflakes migration_linter tests

	@echo -e "${COLOR_BLUE}\n=== Security: Bandit ===\n${NO_COLOR}"
	@poetry run bandit --recursive --quiet --skip B322 migration_linter

	@echo -e "${COLOR_BLUE}\n=== Security: Safety ===\n${NO_COLOR}"
	@poetry run safety check --bare

	@echo -e "${COLOR_BLUE}\n=== Style: isort ===\n${NO_COLOR}"
	@poetry run isort --check migration_linter tests

	@echo -e "${COLOR_BLUE}\n=== Style: Black ===\n${NO_COLOR}"
	@poetry run black --quiet --check migration_linter tests

	@echo -e "${COLOR_GREEN}\n=== All Good! ===${NO_COLOR}"


##     test:    Run tests.
.PHONY: test
test:
	@echo -e "${COLOR_BLUE}=== Pytest ===\n${NO_COLOR}"
	@poetry run pytest --quiet tests

##     test-all:    Run tests across supported Python versions.
.PHONY: test-all
test-all:
	@echo -e "${COLOR_BLUE}=== Tox ===\n${NO_COLOR}"
	@poetry run tox --quiet
