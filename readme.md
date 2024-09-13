# Proj-Dev Brain Games

Bienvenue dans **Proj-Dev Brain Games**, un projet de jeux vidéo avec deux jeux disponibles créé par nous : **Monster-Run**, **Pac-Man**, **Snake The Maze**. Ce projet est développé en utilisant **Pygame**.

## Description

Le projet commence avec une page d'accueil où vous pouvez choisir quel jeu vous voulez jouer : **Monster-Run** ou **Pac-Man**. Il existe également une option pour se connecter avec un compte. Après la connexion, vos données sont enregistrées dans une base de données et vous pouvez accéder à vos statistiques et aux classements des meilleurs scores depuis l'interface.

### Jeux inclus :

- **Monster-Run** : Un jeu d'action rapide où vous devez éviter projectils projeté par les monstres.
- **Pac-Man** : Le jeu d'arcade classique où vous mangez des points tout en évitant les fantômes.
- **Snake The Maze** : Un jeu mélangeant le fameux jeu python snake avec un touche d'inspiration du film Maze Runner ou je but serra de sortir du labyrithe.

## Installation

### 1. Installer les dépendances

Le projet utilise **Pygame**. Pour installer **Pygame**, vous devez exécuter la commande suivante :

```bash
pip install pygame

```

# Exécuter le jeu
Pour lancer les jeux, exécutez simplement votre fichier principal, par exemple 

```bash
python main.py
```


# Résolution du problème des chemins d'image dans PyCharm

Lorsque vous utilisez des chemins relatifs pour les images (par exemple ./src/images/...), ceux-ci fonctionnent correctement sous VSCode mais peuvent poser problème sous PyCharm. Cela est dû au fait que le répertoire de travail par défaut dans PyCharm peut être différent.

# Solution
Pour résoudre ce problème dans PyCharm, vous devez configurer manuellement le répertoire de travail. Voici comment faire :

Allez dans File > Settings.
Naviguez jusqu'à Project > Python Interpreter > Edit Configurations.
Dans la section Working Directory, assurez-vous que le répertoire est défini sur le dossier racine de votre projet. Cela garantit que les chemins relatifs fonctionneront correctement.


###

# Fonctionnalités à ajouter

Connexion avec un compte : Se connecter pour enregistrer vos données et consulter vos statistiques.
Classements : Consultez les meilleurs scores pour chaque jeu.
Interface de sélection de jeu : Choisissez entre Monster-Run ou Pac-Man depuis la page d'accueil.
Technologies utilisées
Pygame : Bibliothèque utilisée pour développer les jeux.
Base de données : Utilisée pour stocker les scores et les statistiques des utilisateurs.

### 


# Technologies utilisées
Pygame : Bibliothèque utilisée pour développer les jeux.
Base de données : Utilisée pour stocker les scores et les statistiques des utilisateurs.