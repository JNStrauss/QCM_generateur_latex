# LaTeX QCM Generator

Generates anti-cheating QCM PDFs in LaTeX from a document of questions and correct answers.

## Description

This project automatically generates multiple-choice questionnaires (QCM) in LaTeX. The script takes a text file containing questions and possible answers and generates several versions of the QCM to minimize cheating risks.

## Features

- Generates multiple versions of QCM from a question file.
- Shuffles questions and answers for each version.
- Automatically creates PDF files using `pdflatex`.
- Supports basic latex syntax for questions

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [LaTeX](https://www.latex-project.org/get/)

## Installation

### Just for subjects generation

You might need to change this line

```py
from qcm_generator.main_cli import generate_subjects
```

to

```py
from main_cli import generate_subjects
```

### For development

Clone the repository and install the required dependencies:

```sh
git clone https://github.com/toby-bro/latex_QCM_generator.git
cd latex_QCM_generator
make install
```

## Usage

### From GUI

Provided the required packages are installed then a double click on the `main_gui.py` should do the trick

### From CLI

1. Create a `questions.txt` file in the project root containing the following information:

    ```txt
    QCM Title
    Author
    School
    Course
    Date

    Q1. First question?
    Answer A
    Answer B
    Answer C

    Q2. Second question?
    Answer A
    Answer B
    Answer C
    ```

2. Run the Python script from CLI:

    ```sh
    python qcm_generator/main_cli.py
    ```

3. The generated PDF files will be located in the `subjects` directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
