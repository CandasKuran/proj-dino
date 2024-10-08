
# Jeu de Course avec Pygame

## Description
Ce jeu est un jeu de course simple où le joueur contrôle un personnage qui court et doit éviter des obstacles. Le but du jeu est d'obtenir le meilleur score possible en sautant par-dessus des obstacles et en utilisant une "position Superman" pour franchir des obstacles en hauteur. Le jeu se complique à mesure que le score augmente avec de nouveaux obstacles et une vitesse croissante.

## Fonctionnalités
- Animation de course pour le personnage
- Saut et "position Superman" pour éviter les obstacles
- Différents types d'obstacles (au sol, en hauteur, surprises)
- Augmentation de la difficulté au fur et à mesure du jeu (vitesse et gravité)
- Écran de fin avec la possibilité de rejouer ou de quitter

## Commandes
- **Flèche Haut (↑)** : Faire sauter le personnage
- **Barre d'Espace** : Activer la "position Superman" et un saut en longueur
- **Souris** : Sur l'écran de fin de jeu, cliquez sur les boutons pour rejouer ou quitter.

## Dépendances
- Pygame doit être installé pour exécuter le jeu. Vous pouvez l'installer via pip :
  ```bash
  pip install pygame
  ```

## Instructions d'Installation
1. Clonez le dépôt de code ou téléchargez-le.
2. Assurez-vous que Pygame est installé sur votre système.
3. Placez les images du jeu dans le répertoire `./src/games/gameDino/img/` :
   - `h1.png`, `h2.png`, `h3.png` pour les animations du personnage.
   - `h1-superMan.png` pour la position Superman.
   - `obs1.png`, `obs2.png`, `obs3.png` pour les obstacles.

4. Exécutez le jeu avec la commande suivante :
   ```bash
   python main.py
   ```

## Structure du Jeu
Le jeu contient les éléments suivants :
- **Personnage principal** : Une animation simple de course avec trois images différentes.
- **Obstacles** : Trois types d'obstacles apparaissant à différents moments et à différentes hauteurs.
- **Difficulté croissante** : La couleur de fond, la vitesse du jeu et la gravité augmentent au fur et à mesure que le score du joueur augmente.

## Personnalisation
- Vous pouvez ajuster la vitesse du jeu, la gravité et les paramètres d’apparition des obstacles en modifiant les variables correspondantes dans le code :
  - `vitesse_jeu`
  - `gravite`
  - `obstacle_chance`

