install: install-prod

install-dev:
	uv sync --all-extras

install-prod:
	uv sync --all-extras --no-dev

build:
	uv build

publish:
	uv publish --token $(token)

lint:
	uv run ruff check --select I --fix .
	uv run ruff format .

typecheck:
	uv run mypy nerva

.PHONY: env rmenv install install-dev install-prod build publish lint typecheck
.DEFAULT_GOAL := build
