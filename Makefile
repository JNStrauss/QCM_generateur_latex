all: run

BASE_DIR = qcm_generator
OUTPUT_DIR = $(BASE_DIR)/sujets

run:
	python $(BASE_DIR)/main_latex.py

clean:
	rm -rf $(OUTPUT_DIR)/*.tex $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.out $(OUTPUT_DIR)/aux_files

purge:
	rm -rf $(OUTPUT_DIR)


.PHONY: all run clean purge