import pygame
import sys
import random
import time
import math

def final_boss_loop():
    pygame.init()

    LARGEUR, HAUTEUR = 1100, 800
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    BLEU = (0, 0, 255)

    TAILLE_CARRE = 50
    TAILLE_BOSS = 80  # Taille des petites images des boss dans les coins

    # Charger les images des boss (versions réduites)
    boss_images = []
    boss_image_paths = ['./src/games/monster-run/images/1.png', './src/games/monster-run/images/2.png', './src/games/monster-run/images/3.png', './src/games/monster-run/images/4.png', './src/games/monster-run/images/5.png']
    for path in boss_image_paths:
        boss_image = pygame.image.load(path)
        boss_image = pygame.transform.scale(boss_image, (TAILLE_BOSS, TAILLE_BOSS))
        boss_images.append(boss_image)

    # Positions des boss (dans les quatre coins de l'écran)
    boss_positions = [
        (0, 0),  # Coin supérieur gauche
        (LARGEUR - TAILLE_BOSS, 0),  # Coin supérieur droit
        (0, HAUTEUR - TAILLE_BOSS),  # Coin inférieur gauche
        (LARGEUR - TAILLE_BOSS, HAUTEUR - TAILLE_BOSS)  # Coin inférieur droit
    ]

    # Charger plusieurs images pour les projectiles (les objets envoyés vers le centre)
    projectile_images = []
    projectile_image_paths = ['./src/games/monster-run/images/chc.png', './src/games/monster-run/images/cisco.png', './src/games/monster-run/images/icescrum.png', './src/games/monster-run/images/nas.png', './src/games/monster-run/images/horlage.png']
    for path in projectile_image_paths:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (50, 50))  # Redimensionner chaque image à 50x50
        projectile_images.append(image)

    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Final Boss")

    carre_x = LARGEUR // 2  # Position du joueur au centre de l'écran
    carre_y = HAUTEUR // 2

    vitesse_x = 0
    vitesse_y = 0

    projectiles = []  # Chaque projectile aura [x, y, vitesse_x, vitesse_y, image]
    horloge = pygame.time.Clock()

    police = pygame.font.SysFont(None, 40)

    def verifier_collision(carre_rect, objets):
        for objet in objets:
            image = objet[4]  # Obtenir l'image du projectile
            objet_rect = pygame.Rect(objet[0], objet[1], image.get_width(), image.get_height())
            if carre_rect.colliderect(objet_rect):
                return True
        return False

    # Fonction pour afficher le temps restant
    def afficher_infos(temps_restant):
        infos = f"Temps restant: {temps_restant:.0f} sec"
        message = police.render(infos, True, NOIR)
        ecran.blit(message, [10, 10])

    # Fonction pour générer les projectiles qui vont vers le centre
    def creer_projectile(dep_x, dep_y, cible_x, cible_y):
        angle = math.atan2(cible_y - dep_y, cible_x - dep_x)  # Calculer l'angle pour viser le centre
        vitesse_projectile = 5  # Vitesse des projectiles
        image = random.choice(projectile_images)  # Sélectionner une image aléatoire pour chaque projectile
        return [dep_x, dep_y, vitesse_projectile * math.cos(angle), vitesse_projectile * math.sin(angle), image]

    temps_initial = time.time()
    while True:
        temps_courant = time.time()
        temps_ecoule = temps_courant - temps_initial

        temps_restant = 15 - temps_ecoule  # Le joueur doit survivre 15 secondes
        ecran.fill(BLANC)

        afficher_infos(temps_restant)

        if temps_ecoule > 15:
            return True  # Le joueur a survécu, on termine le niveau

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_LEFT:
                    vitesse_x = -5
                if evenement.key == pygame.K_RIGHT:
                    vitesse_x = 5
                if evenement.key == pygame.K_UP:
                    vitesse_y = -5
                if evenement.key == pygame.K_DOWN:
                    vitesse_y = 5

            if evenement.type == pygame.KEYUP:
                if evenement.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    vitesse_x = 0
                if evenement.key in [pygame.K_UP, pygame.K_DOWN]:
                    vitesse_y = 0

        # Mettre à jour la position du joueur
        carre_x += vitesse_x
        carre_y += vitesse_y

        carre_x = max(0, min(carre_x, LARGEUR - TAILLE_CARRE))
        carre_y = max(0, min(carre_y, HAUTEUR - TAILLE_CARRE))

        # Créer plusieurs projectiles à partir des positions des boss (coins) vers le centre
        if random.randint(0, 100) < 5:  # Contrôler la fréquence des projectiles
            for pos in boss_positions:
                for _ in range(5):  # Chaque boss envoie 5 projectiles
                    offset_x = random.randint(-50, 50)  # Générer des petites variations dans les positions
                    offset_y = random.randint(-50, 50)
                    projectiles.append(creer_projectile(pos[0] + offset_x, pos[1] + offset_y, carre_x, carre_y))

        # Mettre à jour la position des projectiles
        for projectile in projectiles:
            projectile[0] += projectile[2]  # Déplacement horizontal
            projectile[1] += projectile[3]  # Déplacement vertical

        projectiles = [p for p in projectiles if 0 <= p[0] <= LARGEUR and 0 <= p[1] <= HAUTEUR]  # Garder les projectiles à l'écran

        carre_rect = pygame.Rect(carre_x, carre_y, TAILLE_CARRE, TAILLE_CARRE)
        if verifier_collision(carre_rect, projectiles):
            ecran.fill(BLANC)
            pygame.display.flip()
            pygame.time.delay(2000)
            return False  # Le joueur est touché, fin du jeu

        # Dessiner le joueur
        pygame.draw.rect(ecran, BLEU, carre_rect)

        # Dessiner les boss dans les coins
        for i, pos in enumerate(boss_positions):
            ecran.blit(boss_images[i], pos)

        # Dessiner les projectiles
        for projectile in projectiles:
            ecran.blit(projectile[4], (projectile[0], projectile[1]))  # Dessiner chaque projectile avec son image correspondante

        pygame.display.flip()
        horloge.tick(60)
