import os.path
from random import sample, shuffle
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

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
    tq = TITRE
    tr = ''
    for qi in range(len(liste_qcm[i])):
        noms = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        tq += '\n \n' + str(qi + 1) + '.' + liste_qcm[i][qi].titre
        for k in liste_qcm[i][qi].lq:
            tq += '\n' + str(noms.pop(0)) + ' ' + k
        tr += '\n' + str(qi + 1) + liste_qcm[i][qi].lr
    f = open(path(f'sujet{i + 1}.txt'), 'w', encoding='UTF8')
    f.write(tq)
    f.close()
    
    f = open(path('corriges.txt'), 'a', encoding='UTF8')
    f.write(f'\n \n sujet {i + 1} : \n')
    f.write(tr)
    f.close()
    