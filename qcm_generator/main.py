import logging
import os
import re
import subprocess
from random import sample

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

script_dir = os.path.dirname(__file__)
num_different_subjects = 4

latex_top = r"""
\documentclass[12pt]{{article}}
\usepackage{{ae,lmodern}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{geometry}}
\usepackage{{amsmath}}
\usepackage[french]{{babel}}
\usepackage{{amsfonts}}
\usepackage{{dsfont}}
\usepackage[normalem]{{ulem}}
\usepackage{{amssymb}}
\usepackage{{xcolor}}
\usepackage{{enumitem}}
\usepackage{{fancyhdr}}
\usepackage{{lastpage}}
\geometry{{hmargin=3cm,vmargin=2.5cm}}
\usepackage{{setspace}}
\author{{{author}}}
\pagestyle{{fancy}}
\renewcommand\headrulewidth{{1pt}}
\fancyhead[L]{{\textbf{{{subject}}}}}
\fancyhead[R]{{{school}}}
\fancyfoot[C]{{\thepage /\pageref{{LastPage}}}}
\title{{{title}}}
\date{{{date}}}
\begin{{document}}
\maketitle
\onehalfspacing
"""


class Question:
    possible_answers: list[str]
    question: str

    def __init__(self, title: str, possible_answers: list[str]):
        self.question = title
        self.possible_answers = possible_answers

    def mix_answers(self) -> None:
        order = sample(list(range(len(self.possible_answers))), len(self.possible_answers))
        self.possible_answers = [self.possible_answers[i] for i in order]


def path(rel_path: str) -> str:
    return os.path.join(script_dir, rel_path)


def read_file(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='UTF8') as file:
        return file.readlines()


def write_file(file_path: str, content: str) -> None:
    with open(file_path, 'w', encoding='UTF8') as file:
        file.write(content)


def parse_questions(raw_lines: list[str]) -> tuple[list[str], list[list[str]]]:
    i = 0
    while raw_lines[i][0] != 'Q' and i < len(raw_lines):
        i += 1

    if i == len(raw_lines):
        raise Exception('Bad question typography: the line must start with "Q2."')

    k = raw_lines[i].index('.') + 1
    questions = []
    choices: list[list[str]] = []

    raw_lines = [re.sub(r'(?<!\\)%', r'\%', line) for line in raw_lines]

    for line in raw_lines:
        if line.startswith('Q'):
            questions.append(line[k:].strip())
            choices.append([])
        elif line.strip() and questions:
            choices[-1].append(line.strip())

    return questions, choices


# Regex pattern to match relative \includegraphics (with or without options)
INCLUDE_PATTERN = r'\\includegraphics(?:\[(.*?)\])?\{([^:/].*?)\}'


def transform_include_path(match: re.Match) -> str:
    options = match.group(1) if match.group(1) else ''
    relative_path = match.group(2)
    new_path = f'../../{relative_path}'
    if options:
        return f'\\includegraphics[{options}]{{{new_path}}}'
    return f'\\includegraphics{{{new_path}}}'


def transform_image_includes(latex_content: str) -> str:
    return re.sub(INCLUDE_PATTERN, transform_include_path, latex_content)


def generate_qcm(questions: list[Question], num_subjects: int) -> list[list[Question]]:
    return [sample(questions, len(questions)) for _ in range(num_subjects)]


def clean() -> None:
    base_path = os.path.dirname(__file__)
    full_output_dir = os.path.join(base_path, 'subjects')
    extensions = ['.tex', '.log', '.aux', '.out']
    aux_files_dir = os.path.join(full_output_dir, 'aux_files')

    for root, _, files in os.walk(full_output_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                os.remove(os.path.join(root, file))

    if os.path.isdir(aux_files_dir):
        for root, dirs, files in os.walk(aux_files_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(aux_files_dir)


def create_latex_files(liste_qcm: list[list[Question]], latex_top: str) -> None:
    aux_dir = path('subjects/aux_files')
    output_dir = path('subjects')

    os.makedirs(aux_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    for i, qcm in enumerate(liste_qcm):
        for quest in qcm:
            quest.mix_answers()

        tq = f'{latex_top}\n\\textsc{{Sujet {i + 1}}}\n\\begin{{enumerate}}\n'

        for question in qcm:
            tq += f'\n\\item {question.question}\n\\begin{{enumerate}}'
            for k in question.possible_answers:
                tq += f'\n\\item {k}'
            tq += '\n\\end{enumerate}\n\\vspace{0.5cm}'

        tq = transform_image_includes(tq)

        sujet_path = path(f'subjects/aux_files/sujet{i + 1}.tex')
        write_file(sujet_path, tq + '\n\\end{enumerate}\n\\end{document}')

        result = subprocess.run(  # noqa: S603
            [  # noqa: S607
                'pdflatex',
                '-interaction=nonstopmode',
                f'-output-directory={output_dir}',
                sujet_path,
            ],
            capture_output=True,
            check=False,
        )

        if result.returncode != 0:
            logging.error(result.stdout)
            return

        if result.stdout:
            logging.debug(result.stdout)
        if result.stderr:
            logging.error(result.stderr)


def main() -> None:
    raw_questions = read_file(path('questions.txt'))

    title = 'QCM'
    author = ''
    school = ''
    course = ''
    date = ''

    for i, line in enumerate(raw_questions):
        if not line.strip():
            break
        if i == 0:
            title = line.strip()
        elif i == 1:
            author = line.strip()
        elif i == 2:
            school = line.strip()
        elif i == 3:
            course = line.strip()
        elif i == 4:
            date = line.strip()

    head_lines = len({title, author, school, course, date})
    if date == '':
        logging.warning('Title, author, school, course, or date information is missing in questions.txt')

    raw_questions = raw_questions[head_lines:]

    formatted_title_header = latex_top.format(title=title, author=author, subject=course, school=school, date=date)

    question_list, possible_choices = parse_questions(raw_questions)

    questions = [Question(question_list[i], possible_choices[i]) for i in range(len(question_list))]
    liste_qcm = generate_qcm(questions, num_different_subjects)

    create_latex_files(liste_qcm, formatted_title_header)

    clean()


if __name__ == '__main__':
    main()