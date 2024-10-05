all: run

BASE_DIR = qcm_generator
OUTPUT_DIR = $(BASE_DIR)/subjects

run:
	python $(BASE_DIR)/main_cli.py

clean:
	rm -rf $(OUTPUT_DIR)/*.tex $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.out $(OUTPUT_DIR)/aux_files
	rm $(BASE_DIR)/debug.log

purge: clean
	rm -rf $(OUTPUT_DIR)
	rm $(BASE_DIR)/questions.txt

test:
	poetry run pytest

lint:
	poetry run ruff check $(BASE_DIR)
	poetry run black $(BASE_DIR)

types:
	poetry run mypy $(BASE_DIR)

check: test lint types

install:
	poetry lock
	poetry install
	pre-commit install

.PHONY: all run clean purge test check lint types install