all: run

OUTPUT_DIR = sujets

run:
	python app/main_latex.py

clean:
	rm -rf $(OUTPUT_DIR)/*.tex $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.out $(OUTPUT_DIR)/aux_files

purge:
	rm -rf $(OUTPUT_DIR)


.PHONY: all run clean purge