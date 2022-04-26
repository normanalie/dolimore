# Generation automatique de contrats de cession
Un utilisateur loggé doit remplir un formulaire et telecharger un contrat de cession généré automatique selon un modèle.
Le fichier generé est un PDF de préference, sinon un ODT.
Le contrat est généré sur la base d'un modle ODT fournit par l'admin.


## Modèle
L'admin upload un document .ODT avec des mots #xxx. 
L'algorithme detecte les mots #xxx, #aaa ... et génère automatique un champs de formulaire pour chaque nouveau keyword:

xxx: <input type="text" required>

aaa: <input type="text" required>


## Warnings
Les keywords doivent être ajoutés avec LibreOffice. Word ne gènere pas une structure XML cohérente au moment de l'export en ODT. Cela peut empecher la detection des keywords. 
