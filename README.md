# Centre-logiciel
Version 2024.11.12 du centre logiciel - comment l'installer :
- Télécharger Python
- Télécharger le fichier `Centre Logiciel 2024.11.12`.
- Avant d'exécuter le fichier, intaller `pilow`. Pour l'installer, aller sur cmd et taper la commande `pip install pillow`.
- Et puis vous êtes prêt à créer votre blibliothèque d'application.

# Préparer votre centre logiciel
Comment préparer votre centre logiciel :
- Dans l'interpréteur `Python`, ouvrez le fichier `Centre Logiciel 2024.11.12`.
- Dans le code du centre logiciel, il y a cette commande : `self.admin_password = "admin123"`, changez-la par un mot autre mot de passe.
- Ce code vous sera utile pour ajouter un application ou supprimer un application.
- Maintenant vous pouvez l'ouvrir.

# C'est quoi le fichier Center.db ?
Ce fichier est en faite une base de donnés des applications. c'est de caractères qui enregistrera :
( ex : Air server, fichier d'installation, description, etc).

Conseil pour ne pas voir ce fichier faites un dossier et mettez les deux fichier dans le dossier puis, faites un raccourci dans le bureau :
( ex : dans le disque sur, dossier nommée : Centre logiciel, et mettez les deux fichiers dedans. Puis faites un raccourci de l'exe sur le bureau).

# Comment faire si vous devez installer le centre logiciel sur un domaine ?
Sur le serveur du domaine, vous pouvez faire un partage d'un dossier que vous pouvez nommer `Applications - Centre logiciel`.

Puis vous pouvez mettre des dossiers avec l'application et l'image.

Et vous pouvez mettre le partage avec les autres ordinateurs. Puis toujours copier le fichier `Center.db` sur les autres ordinateur comme nous l'avons fait avant. (Pour éviter de remettre les applications)


