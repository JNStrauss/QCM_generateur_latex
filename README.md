# QCM Generator

## Features

- Randomizes the order of questions
- Randomizes the answer choices
- Generates files for easy correction

The `.pdf` and `corrige.txt` files will be generated in the `/sujets` folder, while other files (notably `.txt` files) will be in the `/sujet/aux` folder.

## Prerequisites

- Install MikTeX on your computer (ensure `pdflatex` is in the PATH, the installer usually handles this).
- Ensure all required packages are installed:
  - The simplest way is to open your favorite LaTeX development interface, compile the `test.tex` file in the folder, and accept any package installation prompts from MikTeX. Once done, the program is ready to run. You can then delete all files starting with `test.` If this doesn't work, you have three options:
    - Check that in MikTeX Console: `Settings` -> `Package Installation` -> `Ask me` is selected, not `Never`.
    - Use `main_moche.py` and manually copy-paste into your WYSIWYG editor, saving all files manually.
    - Write the QCM manually.

## Rules

The `main_latex.py` program generates different questionnaires from an initial set of questions. Place it in a folder containing `questions.txt` and `reponses.txt`.

### Typographic Rules

- The first line of `questions.txt` should be the title of the quiz.
- Questions should start with `Q2.` (replace `2` with your desired number; this number is for your convenience and does not affect the program). The `.` is necessary to identify the start of a question.
- Avoid leaving blank lines, as the program will interpret them as possible answers. Single line breaks are understood, but lines filled with tabs or spaces will be interpreted as answer choices.

- The `reponses.txt` file can include the quiz title, but the program ignores it.
- Answers should start with `2.` (replace `2` with your desired number), and the `.` is necessary.

### Common Issues

- Do not delete the `aux_files` or `sujets` folders.
- In LaTeX, `%` introduces comments, so in a mathematical formula, it must be preceded by a backslash `\`.

### Advanced Users

You can type all questions in LaTeX and modify the packages used (add or remove as needed). The default packages are those I commonly use but are not essential for the QCM generator.

If there are compilation issues, try compiling the files manually in your favorite TeX editor to identify rule violations (often illegal characters like `%`, `*`, `µ`, `°`, etc.). If other issues arise, run `main_latex.py` in your preferred IDE to get verbose output and save time.

