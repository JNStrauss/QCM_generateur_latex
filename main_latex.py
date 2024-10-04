import os
from string import ascii_lowercase
from random import sample
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

script_dir = os.path.dirname(__file__)
nombre_de_sujets_différents = 4

latex_top = r"""
\documentclass[12pt]{article}
\usepackage{ae,lmodern}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{amsmath}
\usepackage[french]{babel}
\usepackage{amsfonts}
\usepackage{dsfont}
\usepackage[normalem]{ulem}
\usepackage{amssymb}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{lastpage}
\geometry{hmargin=3cm,vmargin=2.5cm}
\usepackage{setspace}
\author{Professeur}
\pagestyle{fancy}
\renewcommand\headrulewidth{1pt}
\fancyhead[L]{\textbf{Enseignement scientifique}}
\fancyhead[R]{Lycée}
\fancyfoot[C]{\thepage /\pageref{LastPage}}
"""

alphabet = ascii_lowercase

class Question:
    def __init__(self, intitulé: str, liste_questions: list, liste_reponses: str):
        self.titre = intitulé
        self.lq = liste_questions
        self.lr = liste_reponses.strip()

    def mix_answers(self):
        order = sample(list(range(len(self.lq))), len(self.lq))
        bons_num = [alphabet.index(i) for i in self.lr]
        self.lq = [self.lq[i] for i in order]
        self.lr = ''.join(sorted(alphabet[order.index(i)] for i in bons_num))

def path(rel_path):
    return os.path.join(script_dir, rel_path)

def read_file(file_path):
    with open(file_path, 'r', encoding='UTF8') as file:
        return file.readlines()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='UTF8') as file:
        file.write(content)

def parse_questions(vrac):
    i = 0
    while vrac[i][0] != 'Q' and i < len(vrac):
        i += 1

    if i == len(vrac):
        raise Exception('Mauvaise typographie des questions : il faut que la ligne commence par "Q2."')

    k = vrac[i].index('.') + 1
    liste_questions = []
    liste_possibilites = []

    for ligne in vrac:
        ligne = ligne.replace('%', r'$\%$')
        if ligne.startswith('Q'):
            liste_questions.append(ligne[k:].strip())
            liste_possibilites.append([])
        elif ligne.strip() and liste_questions:
            liste_possibilites[-1].append(ligne.strip())

    return liste_questions, liste_possibilites

def parse_reponses(vrac):
    liste_bonnes_reponses = []
    for ligne in vrac:
        ligne = ligne.strip()
        if ligne and (ligne[1] == '.' or (ligne[2] == '.' and ligne[1].isdigit())):
            liste_bonnes_reponses.append(ligne.split('.', 1)[1].strip())
    return liste_bonnes_reponses

def generate_qcm(questions, nombre_de_sujets_différents):
    return [sample(questions, len(questions)) for _ in range(nombre_de_sujets_différents)]

def create_latex_files(liste_qcm, latex_top):
    for i, qcm in enumerate(liste_qcm):
        for quest in qcm:
            quest.mix_answers()

        tq = f"{latex_top}\n\\textsc{{Sujet {i + 1}}}\n\\begin{{enumerate}}\n"
        tr = ''

        for qi, question in enumerate(qcm):
            tq += f"\n\\item {question.titre}\n\\begin{{enumerate}}"
            for k in question.lq:
                tq += f"\n\\item {k}"
            tq += "\n\\end{enumerate}\n\\vspace{0.5cm}"
            tr += f"\n{qi + 1}. {question.lr}"

        sujet_path = path(f'sujets/aux_files/sujet{i + 1}.tex')
        write_file(sujet_path, tq + '\n\\end{enumerate}\n\\end{document}')

        os.system(f"pdflatex -aux-directory=\"{path('sujets/aux_files')}\" -output-directory=\"{path('sujets')}\" -verbose {sujet_path}")

        with open(path('sujets/corriges.txt'), 'a', encoding='UTF8') as f:
            f.write(f'\n\nsujet {i + 1} : \n{tr}')

def main():
    vrac_questions = read_file(path('questions.txt'))
    vrac_reponses = read_file(path('reponses.txt'))

    TITRE = vrac_questions[0].strip()
    latex_top_with_title = latex_top + f'\n\\title{{{TITRE}}}\n\\makeindex\n\\begin{{document}}\n\\maketitle\n\\onehalfspacing'

    liste_questions, liste_possibilites = parse_questions(vrac_questions)
    liste_bonnes_reponses = parse_reponses(vrac_reponses)

    questions = [Question(liste_questions[i], liste_possibilites[i], liste_bonnes_reponses[i]) for i in range(len(liste_questions))]
    liste_qcm = generate_qcm(questions, nombre_de_sujets_différents)

    write_file(path('sujets/corriges.txt'), '')
    create_latex_files(liste_qcm, latex_top_with_title)

if __name__ == "__main__":
    main()
