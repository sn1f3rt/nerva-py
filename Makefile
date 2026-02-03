env:
	uv venv

rmenv:
	rm -rf .venv

install: install-prod

install-dev:
	uv sync --all-extras

install-prod:
	uv sync --all-extras --no-dev

build:
	uv build

publish:
	uv publish --token $(token)

format:
	ruff check --select I --fix .
	ruff format .

.PHONY: env rmenv install install-dev install-prod build publish format
.DEFAULT_GOAL := build
