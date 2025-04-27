.DEFAULT_GOAL := help
POETRY_RUN = poetry run
TEST = pytest $(arg)
CODE = app tests

COVERAGE_REPORT = htmlcov/status.json
COBERTURA_REPORT = cobertura.xml
COVERAGE_REPORT_FOLDER = $(shell dirname $(COVERAGE_REPORT))

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Runs pytest with coverage
	$(POETRY_RUN) $(TEST) --cov=./

.PHONY: test-fast
test-fast: ## Runs pytest with exitfirst
	$(POETRY_RUN) $(TEST) --exitfirst

.PHONY: test-failed
test-failed: ## Runs pytest from last-failed
	$(POETRY_RUN) $(TEST) --last-failed

test-with-coverage-report: ## Runs pytest with coverage report
	$(POETRY_RUN) $(TEST) --cov --cov-report term --cov-report xml:$(COBERTURA_REPORT) --cov-report html:$(COVERAGE_REPORT_FOLDER)
	@if [ ! -f $(COVERAGE_REPORT) ]; then\
		echo 'Coverage report not found: $(COVERAGE_REPORT)';\
	fi

.PHONY: lint
lint: ## Lint code
	$(POETRY_RUN) pylint --jobs 1 --rcfile=pyproject.toml $(CODE)
	$(POETRY_RUN) ruff check $(CODE)
	$(POETRY_RUN) mypy $(CODE)
	$(POETRY_RUN) black --check $(CODE)
	$(POETRY_RUN) pytest --dead-fixtures --dup-fixtures

.PHONY: format
format: ## Formats all files
	$(POETRY_RUN) black $(CODE)
	$(POETRY_RUN) ruff check --fix $(CODE)

.PHONY: check
check: format lint test ## Format and lint code then run tests

.PHONY: ci
ci: lint test-with-coverage-report ## Lint code then run tests with coverage report

.PHONY: install
install: ## Install dependencies
	poetry install --no-interaction --no-ansi

run-api: ## Run app
	ENV=local $(POETRY_RUN) uvicorn app.api.app:create_app --reload

run-environment: ## Run environment
	@export $$(cat envs/common.env | xargs); export $$(cat envs/local.env | xargs); docker compose up -d

stop-environment: ## Stop environment
	@export $$(cat envs/common.env | xargs); export $$(cat envs/local.env | xargs); docker compose down

grev:
	poetry run alembic revision --autogenerate -m "$(message)"

urev:
	poetry run alembic upgrade head

drev:
	poetry run alembic downgrade -1
