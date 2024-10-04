import logging
import os
import re
import subprocess
from random import sample
from string import ascii_lowercase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

script_dir = os.path.dirname(__file__)
nb_different_subjects = 4

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

alphabet = ascii_lowercase


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


def parse_questions(vrac: list[str]) -> tuple[list[str], list[list[str]]]:
    i = 0
    while vrac[i][0] != 'Q' and i < len(vrac):
        i += 1

    if i == len(vrac):
        raise Exception('Mauvaise typographie des questions : il faut que la ligne commence par "Q2."')

    k = vrac[i].index('.') + 1
    questions = []
    choices: list[list[str]] = []

    vrac = [re.sub(r'(?<!\\)%', r'\%', line) for line in vrac]

    for line in vrac:
        if line.startswith('Q'):
            questions.append(line[k:].strip())
            choices.append([])
        elif line.strip() and questions:
            choices[-1].append(line.strip())

    return questions, choices


def generate_qcm(questions: list[Question], num_subjects: int) -> list[list[Question]]:
    return [sample(questions, len(questions)) for _ in range(num_subjects)]


def create_latex_files(liste_qcm: list[list[Question]], latex_top: str) -> None:
    aux_dir = path('sujets/aux_files')
    output_dir = path('sujets')

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

        sujet_path = path(f'sujets/aux_files/sujet{i + 1}.tex')
        write_file(sujet_path, tq + '\n\\end{enumerate}\n\\end{document}')

        subprocess.run(  # noqa: S603
            [  # noqa: S607
                'pdflatex',
                f'-aux-directory={aux_dir}',
                f'-output-directory={output_dir}',
                '-verbose',
                sujet_path,
            ],
            check=True,
        )


def main() -> None:
    vrac_questions = read_file(path('questions.txt'))

    try:
        title = vrac_questions[0].strip()
        author = vrac_questions[1].strip()
        school = vrac_questions[2].strip()
        course = vrac_questions[3].strip()
        date = vrac_questions[4].strip()
    except IndexError:
        logging.warning('Title, author, school, course, or date information is missing in questions.txt')
        title = 'Default Title'
        author = 'Default Author'
        course = 'Default Subtitle'
        school = 'Default School'
        date = 'Default Date'

    latex_top_with_title = latex_top.format(title=title, author=author, subject=course, school=school, date=date)

    liste_questions, liste_possibilites = parse_questions(vrac_questions)

    questions = [Question(liste_questions[i], liste_possibilites[i]) for i in range(len(liste_questions))]
    liste_qcm = generate_qcm(questions, nb_different_subjects)

    create_latex_files(liste_qcm, latex_top_with_title)


if __name__ == '__main__':
    main()
