.PHONY: lint format type test check

lint:
	uv run ruff check .

format:
	uv run ruff format .

type:
	uv run mypy .

test:
	uv run pytest

check: lint type test
