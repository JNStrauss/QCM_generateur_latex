import os.path
from random import sample, shuffle
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
%\author{Jean-Nicolas Strauss} % l'auteur
 %la date (tu peux ne pas la mettre ça ne change rien, il la génère automatiquement)
 % le titre du document

% si tu veux des détails sur les package : va sur ctan.org

\pagestyle{fancy}
\renewcommand\headrulewidth{1pt}
\fancyhead[L]{\textbf{Enseignement scientifique}}
\fancyhead[R]{Lycée Molière}
\fancyfoot[C]{\thepage /\pageref{LastPage}}"""


""" 
Ne pas oublier de rajouter les différents éléments de la tête et de \makeindex \title \begin{document}... et ensuite on finit le truc et on est des bogosses ! 
"""
nombre_de_sujets_différents = 4

def path(rel_path):
    return os.path.join(script_dir, rel_path)


class Question:
    def __init__(self, intitulé, liste_questions, liste_reponses):
        self.titre = intitulé
        self.lq = liste_questions
        self.lr = liste_reponses


file = open(path('questions.txt'), 'r', encoding='UTF8')
vrac = file.readlines()
file.close()
# print(vrac)

TITRE = vrac[0][:-1]

latex_top += f"""
\title{TITRE}
""" + r"""
\makeindex
\begin{document}
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

f = open(path('corriges.txt'), 'w', encoding='UTF8')
f.write('')
f.close()

for i in range(len(liste_qcm)):
    tq = latex_top + r' \\'
    tr = ''
    for qi in range(len(liste_qcm[i])):
        noms = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        tq += '\n' + str(qi + 1) + '.' + liste_qcm[i][qi].titre + r' \\'
        for k in liste_qcm[i][qi].lq:
            tq += '\n' + str(noms.pop(0)) + ' ' + k + r' \\'
        tr += '\n' + str(qi + 1) + liste_qcm[i][qi].lr + r' \\'
    f = open(path(f'sujet{i + 1}.txt'), 'w', encoding='UTF8')
    f.write(tq[:-2] + '\n')
    f.write(r'end{document}')
    f.close()
    
    f = open(path('corriges.txt'), 'a', encoding='UTF8')
    f.write(f'\n \n sujet {i + 1} : \n')
    f.write(tr)
    f.close()
    