import pygame
import sys
import random
import time
# from mainChar import charger_personnage, afficher_personnage_animate, mettre_a_jour_animation


def boss2_loop():
    from mainChar import charger_personnage, afficher_personnage_animate, mettre_a_jour_animation
    pygame.init()

    LARGEUR, HAUTEUR = 1200, 800
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
    boss_image = pygame.image.load('./src/games/monster-run/images/2.png')
    boss_image = pygame.transform.scale(boss_image, (200, 300))  # Redimensionner l'image du boss
    boss_rect = boss_image.get_rect()
    boss_rect.right = LARGEUR  # Aligner à droite de l'écran
    boss_rect.centery = HAUTEUR // 2  # Centrer verticalement


    boss_vitesse_y = 5 

    # Charger l'image pour les projectiles
    projectile_image = pygame.image.load('./src/games/monster-run/images/coeur.png')
    projectile_image = pygame.transform.scale(projectile_image, (75, 75))  # Redimensionner selon les besoins

    
    # Chargement de l'image de fond pour le niveau du boss
    background_image = pygame.image.load('./src/games/monster-run/images/City3.png')
    background_image = pygame.transform.scale(background_image, (LARGEUR, HAUTEUR))


    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Boss Niveau 2")

    carre_x = LARGEUR // 4
    carre_y = HAUTEUR // 2

    vitesse_x = 0
    vitesse_y = 0

    projectiles = []
    horloge = pygame.time.Clock()

    police = pygame.font.SysFont(None, 40)

    # Position initiale de l'arrière-plan
    background_x = 0

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
     # Temps initial pour le niveau
    temps_initial = time.time()
    while True:
        temps_courant = time.time()
        temps_ecoule = temps_courant - temps_initial

        # Calcul du temps restant pour battre le boss
        temps_restant = 10 - temps_ecoule

        # Déplacement de l'arrière-plan
        background_x -= 5  # Vitesse de défilement de l'arrière-plan

        # Affichage de l'arrière-plan en boucle
        ecran.blit(background_image, (background_x, 0))
        ecran.blit(background_image, (background_x + LARGEUR, 0)) 

        # Réinitialisation de l'arrière-plan pour créer un effet de boucle
        if background_x <= -LARGEUR:
            background_x = 0

        # Affichage des informations du boss
        afficher_infos_boss(1, "Boss 2", temps_restant)

        # Si le temps est écoulé, retourner au jeu principal
        if temps_ecoule > 10:
            return True

        # Gérer les événements du jeu (clavier, souris, etc.)
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

        # Mise à jour de la position du personnage principal
        carre_x += vitesse_x
        carre_y += vitesse_y

        # Limiter le mouvement du personnage à l'écran
        carre_x = max(0, min(carre_x, LARGEUR - frames[0].get_width()))
        carre_y = max(0, min(carre_y, HAUTEUR - frames[0].get_height()))

        # Mise à jour de la position du boss (déplacement vertical)
        boss_rect.centery += boss_vitesse_y

        # Inverser la direction du boss s'il atteint les bords de l'écran
        if boss_rect.top <= 0 or boss_rect.bottom >= HAUTEUR:
            boss_vitesse_y = -boss_vitesse_y

        # Création de projectiles à partir du boss
        if random.randint(0, 100) < 3:  # La fréquence de tir des projectiles
            projectile_y = random.randint(0, HAUTEUR - projectile_image.get_height())
            projectiles.append([boss_rect.left, projectile_y])

        # Déplacement des projectiles vers la gauche
        for projectile in projectiles:
            projectile[0] -= 7

        # Supprimer les projectiles sortis de l'écran
        projectiles = [p for p in projectiles if p[0] > -projectile_image.get_width()]

        # Vérifier les collisions entre le personnage et les projectiles
        carre_rect = pygame.Rect(carre_x, carre_y, frames[0].get_width(), frames[0].get_height())
        if verifier_collision(carre_rect, projectiles):
            ecran.fill(GRIS)
            pygame.display.flip()
            pygame.time.delay(2000)
            return False

        # Mise à jour de l'animation du personnage principal
        index_frame, temps_animation = mettre_a_jour_animation(index_frame, temps_animation, intervalle_animation, horloge, frames)

        # Dessiner l'animation du personnage principal
        afficher_personnage_animate(ecran, frames, index_frame, carre_x, carre_y)

        # Dessiner l'image du boss
        ecran.blit(boss_image, boss_rect)

        # Dessiner les projectiles
        for projectile in projectiles:
            ecran.blit(projectile_image, projectile)

        # Rafraîchir l'écran
        pygame.display.flip()
        horloge.tick(60)

