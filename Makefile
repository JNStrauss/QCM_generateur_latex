all: run

BASE_DIR = qcm_generator
OUTPUT_DIR = $(BASE_DIR)/subjects

run:
	python $(BASE_DIR)/main_cli.py

clean:
	rm -rf $(OUTPUT_DIR)/*.tex $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.out $(OUTPUT_DIR)/aux_files

purge:
	rm -rf $(OUTPUT_DIR)

test:
	poetry run pytest

check: test
	poetry run ruff check $(BASE_DIR)
	poetry run mypy $(BASE_DIR)
	poetry run black $(BASE_DIR)


.PHONY: all run clean purge test check