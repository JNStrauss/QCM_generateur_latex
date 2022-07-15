Le fichier main_latex_2.py génère des QCM en pdf à partir de questions en latex. Il génère un nombre fixé (par défaut 4) de QCM différents en 
- Mélangeant l'ordre des questions
- Mélangeant les possibilités de réponse
- Générant le fichier pour que la correction soit aisée

Les .pdf générés seront dans le dossier /sujets et tout le reste (les fichiers .txt notamment seront dans le dossier /sujet/aux)

# Prérequis : 
- avoir MikTeX installé sur son ordinateur (proprement (il faut que pdflatex soit dans le PATH de l'ordinateur, mais normalement le programme d'installation le fait seul))
- avoir tous les paquets qui sont dans le programme : 
le plus simple est d'ouvrir son interface de développement de LaTeX favorite et de compiler le fichier test.tex dans le dossier, et d'accepter dès que MikTeX propose d'installer un package. Une fois cette manip effectuée, plus rien n'est à faire, le programme est prêt à tourner. Une fois cette manip faite vous pouvez supprimer tous les fichiers dont le nom commence par 'test.' S'il n'y arrive pas vous avez trois solutions :
- vérifier que dans miktex console --> paramètres --> installation de paquets--> demandez-moi / settings --> package installation --> ask me - est cochée et pas -jamais- 
- ne se servir que du main_moche.py et tout copier coller dans son WYSIWYG et enregistrer tous les fichiers à la main
- écrire ces QCM à la main

# Règles :
Le programme main_latex2.py va générer des questionnaires différents à partir d'une même batterie de questions initiales
il faut donc le placer dans un dossier dans lequel il y a un document 'questions.txt' et un document 'reponses.txt'


## Règles typographiques : 
- le document questions.txt à pour première ligne le Titre de l'interrogation 
- les questions doivent commencer par 'Q2.' en remplaçant le 2 par le numéro que vous souhaitez (ce chiffre ne sert à rien dans le programme il n'est là que pour votre confort personnel) et le . est nécessaire pour que le programme identifie le début d'une question.
- essayer d'éviter de laisser des lignes blanches sinon mon programme va les interprèter comme des possibilités de réponses (le programme comprend les sauts de ligne simple mais s'il y a une ligne remplie de tab ou d'espaces il va l'interprèter comme une possibilité de réponse)

- le document réponse peut comporter le titre de l'interrogation mais mon programme s'en fiche
- les réponses doivent commencer par '2.' (où vous remplacez 2 par le chiffre de votre choix) mais où le . est nécessaire

- reponses.txt doit finir par un retour à la ligne

### Problèmes réccurents :
- il ne faut pas supprimer le dossier aux ni le dossier sujets


Pour les utilisateurs chevronés : il est bien évidemment possible de taper toutes les questions en LaTeX et de changer tous les package utilisé (en ajouter comme en enlever, j'ai mis par défaut tous ceux qui me servent habituellement mais ils sont loin d'être utiles pour faire fonctionner un générateur de QCM)

Enfin s'il y a un problème dans la compilation des fichiers, n'hésitez pas à essayer de les compiler manuellement dans votre editeur de TeX favorite pour voir quelles sont les règles que vous avez enfreintes (il s'agit souvent de caractères illégaux tels que * ou µ ou °... bref... s'il y a d'autres problèmes faites tourner le fichier main_latex2.py dans votre IDE préféré, où toute la verbose vous sera renvoyée. Gagnez du temps. 
