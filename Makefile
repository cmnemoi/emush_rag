all: setup-env-variables setup-git-hooks install check test build-watch

build-watch:
	docker compose up --build --watch

check: check-format check-lint check-types

check-format:
	uv run ruff format . --diff

check-lint:
	uv run ruff check .

check-types:
	uv run mypy .

index-documents:
	uv run emush_rag/cli/index_documents.py
	scp -r ./chroma cmnemoi@askneron.com:~/www

install:
	uv lock
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

run:
	docker compose up -d --watch

test:
	uv run python -m pytest -v --cov=emush_rag --cov-report=xml

test-fast:
	uv run python -m pytest -v tests/unit tests/integration

upgrade-dependencies:
	uv lock --upgrade

watch:
	docker compose up --watch

.PHONY: all build-watch check check-format check-lint check-types install lint semantic-release setup-env-variables setup-git-hooks test upgrade-dependencies