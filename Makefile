install: install-prod

install-dev:
	uv sync --all-extras

install-prod:
	uv sync --all-extras --no-dev

install-docs:
	uv sync --group docs

build:
	uv build

publish:
	uv publish --token $(token)

lint:
	uv run ruff check --select I --fix .
	uv run ruff format .

typecheck:
	uv run mypy nerva

docs:
	uv run sphinx-build -b html docs docs/_build/html

.PHONY: env rmenv install install-dev install-prod install-docs build publish lint typecheck docs
.DEFAULT_GOAL := build
