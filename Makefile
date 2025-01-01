all: setup-env-variables setup-git-hooks install check test 

check: check-format check-lint check-types

check-format:
	uv run ruff format . --diff

check-lint:
	uv run ruff check .

check-types:
	uv run mypy .

docker-build:
	docker build -t cmnemoi/emush_rag_api:latest .

docker-run:
	docker run -p 8000:8000 cmnemoi/emush_rag_api:latest

install:
	uv lock --locked
	uv sync --locked --group dev --group lint --group test

lint:
	uv run ruff format .
	uv run ruff check . --fix

semantic-release:
	uv run semantic-release version --no-changelog --no-push --no-vcs-release --skip-build --no-commit --no-tag
	uv lock
	git add pyproject.toml uv.lock
	git commit --allow-empty --amend --no-edit 

setup-env-variables:
	cp .env.example .env

setup-git-hooks:
	chmod +x hooks/pre-commit
	chmod +x hooks/pre-push
	chmod +x hooks/post-commit
	git config core.hooksPath hooks

test:
	uv run pytest -v --cov=emush_rag --cov-report=xml

test-fast:
	uv run pytest -v tests/unit tests/integration

upgrade-dependencies:
	uv lock --upgrade

.PHONY: all check check-format check-lint check-types install lint semantic-release setup-env-variables setup-git-hooks test upgrade-dependencies