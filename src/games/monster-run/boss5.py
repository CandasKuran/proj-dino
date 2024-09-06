import pygame
import sys
import random
import time
from mainChar import charger_personnage, afficher_personnage_animate, mettre_a_jour_animation


def boss5_loop():
    pygame.init()

    LARGEUR, HAUTEUR = 1100, 800
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    ROUGE = (255, 0, 0)
    BLEU = (0, 0, 255)
    GRIS = (192, 192, 192)  # #c0c0c0

    # Charger les frames du personnage en mouvement depuis mainChar.py
    frames = charger_personnage()
    index_frame = 0
    temps_animation = 0
    intervalle_animation = 100  # Intervalle entre les frames en millisecondes


    TAILLE_CARRE = 50

    # Charger les images pour le boss et les projectiles
    boss_image = pygame.image.load('./src/games/monster-run/images/5.png')
    boss_image = pygame.transform.scale(boss_image, (200, 300))  # Redimensionner l'image du boss
    boss_rect = boss_image.get_rect()
    boss_rect.right = LARGEUR  # Aligner à droite de l'écran
    boss_rect.centery = HAUTEUR // 2  # Centrer verticalement

    boss_vitesse_y = 5 

    # Charger l'image pour les projectiles
    projectile_image = pygame.image.load('./src/games/monster-run/images/horlage.png')
    projectile_image = pygame.transform.scale(projectile_image, (75, 75))  # Redimensionner selon les besoins

    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Boss Niveau 5")

    carre_x = LARGEUR // 4
    carre_y = HAUTEUR // 2

    vitesse_x = 0
    vitesse_y = 0

    projectiles = []
    horloge = pygame.time.Clock()

    police = pygame.font.SysFont(None, 40)

    def verifier_collision(carre_rect, objets):
        for objet in objets:
            objet_rect = pygame.Rect(objet[0], objet[1], projectile_image.get_width(), projectile_image.get_height())
            if carre_rect.colliderect(objet_rect):
                return True
        return False

    def afficher_infos_boss(niveau, boss_nom, temps_restant):
        infos = f"Niveau {niveau} - Boss: {boss_nom} | Temps restant: {temps_restant:.0f} sec"
        message = police.render(infos, True, NOIR)
        ecran.blit(message, [10, 10])

    temps_initial = time.time()
    while True:
        temps_courant = time.time()
        temps_ecoule = temps_courant - temps_initial

        temps_restant = 10 - temps_ecoule
        ecran.fill(GRIS)

        afficher_infos_boss(1, "Boss 5", temps_restant)

        if temps_ecoule > 10:
            return True

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

        carre_x += vitesse_x
        carre_y += vitesse_y

        carre_x = max(0, min(carre_x, LARGEUR - TAILLE_CARRE))
        carre_y = max(0, min(carre_y, HAUTEUR - TAILLE_CARRE))


        # Mise à jour de la position du boss pour le faire bouger verticalement
        boss_rect.centery += boss_vitesse_y

        # Inverser la direction si le boss atteint les bords supérieur ou inférieur
        if boss_rect.top <= 0 or boss_rect.bottom >= HAUTEUR:
            boss_vitesse_y = -boss_vitesse_y

        if random.randint(0, 100) < 3:  # La fréquence de tir des projectiles
            projectile_y = random.randint(0, HAUTEUR - projectile_image.get_height())
            projectiles.append([boss_rect.left, projectile_y])

        for projectile in projectiles:
            projectile[0] -= 7

        projectiles = [p for p in projectiles if p[0] > -projectile_image.get_width()]

        carre_rect = pygame.Rect(carre_x, carre_y, TAILLE_CARRE, TAILLE_CARRE)
        if verifier_collision(carre_rect, projectiles):
            ecran.fill(GRIS)
            pygame.display.flip()
            pygame.time.delay(2000)
            return False

        # Mettre à jour l'animation du personnage
        index_frame, temps_animation = mettre_a_jour_animation(index_frame, temps_animation, intervalle_animation, horloge, frames)

        # Dessiner l'image animée du personnage
        afficher_personnage_animate(ecran, frames, index_frame, carre_x, carre_y)

        # Dessiner le boss
        ecran.blit(boss_image, boss_rect)

        # Dessiner les projectiles
        for projectile in projectiles:
            ecran.blit(projectile_image, projectile)

        pygame.display.flip()
        horloge.tick(60)
