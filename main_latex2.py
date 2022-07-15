import os
from string import ascii_lowercase
from random import sample, randint
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

latex_top = r"""\documentclass[12pt]{article} % si tu veux faire un truc avec une mise en page type word, si tu veux faire un diaporama passe par \documentclass{beamer}
\usepackage{ae,lmodern} % polices matricielles
\usepackage[utf8]{inputenc} %codage et police
\usepackage[T1]{fontenc} % prise en charge des césures
\usepackage{geometry} % pour changer les marges du document
\usepackage{amsmath} % pour faire des équations 
\usepackage[french]{babel} % pour qu'il accepte les mots français, les caractères fraçais
\usepackage{amsfonts} % polices de maths
\usepackage{dsfont} % pour les symboles des ensembles maths N, Q, R, K...
% \usepackage{ulem} % il sert à barrer, soouligner du texte
\usepackage[normalem]{ulem} % le [normalem] sert à préciser que lorsque je mets \emph{sur du texte} il est en italiqeu au lieu d'être souligné si on ne met pas [normalem] alors \emph{donne du texte souligné}
\usepackage{amssymb} % d'autres symboles de maths
\usepackage{xcolor} % pour pouvoir changer la couleur de la police
\usepackage{enumitem} % pour faire des listes 
\usepackage{fancyhdr} % pour faire les en-têtes et les pieds de page
\usepackage{lastpage} % pour avoir la dernière page
\geometry{hmargin=3cm,vmargin=2.5cm} % je définis les marges
\usepackage{setspace} % pour définir les interlignes 
\author{Professeur} % l'auteur
% \date{} %la date (tu peux ne pas la mettre ça ne change rien, il la génère automatiquement)

% si tu veux des détails sur les package : va sur ctan.org

\pagestyle{fancy}
\renewcommand\headrulewidth{1pt}
\fancyhead[L]{\textbf{Enseignement scientifique}}
\fancyhead[R]{Lycée}
\fancyfoot[C]{\thepage /\pageref{LastPage}}"""


""" 
Ne pas oublier de rajouter les différents éléments de la tête et de \makeindex \title \begin{document}... et ensuite on finit le truc et on est des bogosses ! 
"""
nombre_de_sujets_différents = 4

def path(rel_path):
    return os.path.join(script_dir, rel_path)

alphabet = ascii_lowercase

class Question:
    def __init__(self, intitulé, liste_questions, liste_reponses):
        self.titre = intitulé # un string
        self.lq = liste_questions # une liste
        i = 0
        while liste_reponses[i] == ' ':
            i+=1
        self.lr = liste_reponses[i:] # c'est un string
    
    def mix_answers(self):
        order = sample(list(range(len(self.lq))), len(self.lq))
        bons_num = [alphabet.index(i) for i in self.lr]
        # print(order, bons_num, self.lq, self.lr)
        self.lq = [self.lq[i] for i in order]
        self.lr = [alphabet[order.index(i)] for i in bons_num]
        self.lr.sort()
        self.lr = ''.join(self.lr)
        # print(self.lq, self.lr)
        # print('')


file = open(path('questions.txt'), 'r', encoding='UTF8')
vrac = file.readlines()
file.close()
# print(vrac)

TITRE = vrac[0][:-1]

latex_top += '\n' + r"\title{" + TITRE + r"""}
\makeindex
\begin{document}
\maketitle
\onehalfspacing"""

# Analyse de la ligne : découvrir comment maman a rentré les questions
i = 0
while vrac[i][0] != 'Q' and i < len(vrac):
    i+=1

if i == len(vrac):
    raise Exception('Mauvaise typographie des questions : il faut que la ligne commence par "Q2."')
else:
    k = 0
    while vrac[i][k] != '.':
        k += 1
# k donne le premier caractère intéressant de la question
k += 1


# On va à présent récupérer les intitulés des questions et leurs propositions de réponse
liste_questions = []
liste_possibilites = []
for ligne in vrac:
    if ligne[0] == 'Q':
        liste_questions.append(ligne[k:-1])
        liste_possibilites.append([])
    elif ligne not in ['\n', '\n ', ' \n'] and liste_questions!=[]:
        liste_possibilites[-1].append(ligne[:-1])

# print(liste_possibilites)


# On va à présent récupérer les bonnes réponses pour chaque question
file = open(path('reponses.txt'), 'r', encoding='UTF8')
vrac = file.readlines()
file.close()
# print(vrac)
liste_bonnes_reponses = []
for ligne in vrac:
    if ligne not in ['\n', ' \n', '\n ']:
        if ligne[1] =='.':
            liste_bonnes_reponses.append(ligne[2:-1])

# print(liste_bonnes_reponses)
        
questions = [Question(liste_questions[i], liste_possibilites[i], liste_bonnes_reponses[i]) for i in range(len(liste_questions))]

# On va à présent générer les QCM différents de par le mélange des questions et le mélange des possibilités de réponse
liste_qcm = [sample(sample(questions, len(questions)), len(questions)) for _ in range(nombre_de_sujets_différents)]
    
    
f = open(path('sujets\corriges.txt'), 'w', encoding='UTF8')
f.write('')
f.close()

for i in range(len(liste_qcm)):
    for quest in liste_qcm[i]:
        quest.mix_answers()
    tq = latex_top + '\n' + r' \textsc{Sujet ' + str(i+1) + '}\n' + r'\begin{enumerate}' + '\n'
    tr = ''
    for qi in range(len(liste_qcm[i])):
        tq += '\n' + r'\item ' + liste_qcm[i][qi].titre
        tq += '\n' + r'\begin{enumerate}'
        for k in liste_qcm[i][qi].lq:
            tq += '\n' + r'\item ' + k
        tq += '\n' + r'\end{enumerate}' + '\n' + r'\vspace{0.5cm}' # le vspace est l'espace supplémentaire entre les questions
        tr += '\n' + str(qi + 1) + liste_qcm[i][qi].lr
    f = open(path(r'sujets\aux_files' + f'\sujet{i + 1}.tex'), 'w', encoding='UTF8')
    f.write(tq + '\n')
    f.write('\n' + r'\end{enumerate}' + '\n' + r'\end{document}')
    f.close()
    os.system("pdflatex -aux-directory=\"" + path(r'sujets\aux_files')+ '" -output-directory="' + path('sujets') + '" -verbose ' + path(r'sujets\aux_files' + f'\sujet{i + 1}.tex'))
    f = open(path('sujets\corriges.txt'), 'a', encoding='UTF8')
    
    f.write(f'\n \n sujet {i + 1} : \n')
    f.write(tr)
    f.close()

