import pygame
import random
import sys

# Initialiser Pygame
pygame.init()

# Dimensions de l'écran
LARGEUR, HAUTEUR = 1200, 600
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu de course")

# Couleurs
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)   # Gris clair
GRIS2 = (100, 100, 100)  # Gris foncé
GRIS3 = (50, 50, 50)     # Gris très foncé
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

# Charger les images du personnage (animations)
frame1 = pygame.image.load('./src/games/gameDino/img/h1.png').convert_alpha()
frame2 = pygame.image.load('./src/games/gameDino/img/h2.png').convert_alpha()
frame3 = pygame.image.load('./src/games/gameDino/img/h3.png').convert_alpha()
frames_personnage = [frame1, frame2, frame3]

# Créer les masques du personnage
frame1_mask = pygame.mask.from_surface(frame1)
frame2_mask = pygame.mask.from_surface(frame2)
frame3_mask = pygame.mask.from_surface(frame3)
frames_personnage_masks = [frame1_mask, frame2_mask, frame3_mask]

# Image et masque pour la position Superman
superman_image = pygame.image.load('./src/games/gameDino/img/h1-superMan.png').convert_alpha()
superman_mask = pygame.mask.from_surface(superman_image)

# Obtenir la hauteur du personnage
hauteur_personnage = frame1.get_height()

# Charger les images des obstacles
image_obstacle = pygame.image.load('./src/games/gameDino/img/obs1.png').convert_alpha()
image_obstacle_2 = pygame.image.load('./src/games/gameDino/img/obs2.png').convert_alpha()
image_obstacle_3 = pygame.image.load('./src/games/gameDino/img/obs3.png').convert_alpha()  # Nouvel obstacle

# Ajuster la taille des images des obstacles
largeur_obstacle = 75
hauteur_obstacle = 75
image_obstacle = pygame.transform.scale(image_obstacle, (largeur_obstacle, hauteur_obstacle))
image_obstacle_2 = pygame.transform.scale(image_obstacle_2, (largeur_obstacle, hauteur_obstacle))
image_obstacle_3 = pygame.transform.scale(image_obstacle_3, (largeur_obstacle, hauteur_obstacle))

# Recréer les masques après le redimensionnement
obstacle_mask = pygame.mask.from_surface(image_obstacle)
obstacle_2_mask = pygame.mask.from_surface(image_obstacle_2)
obstacle_3_mask = pygame.mask.from_surface(image_obstacle_3)

# Position initiale du personnage
x_personnage = 50
y_personnage = HAUTEUR - hauteur_personnage  # Positionner le personnage au sol
vitesse_y = 0
vitesse_x = 0  # Vitesse horizontale
sauter = False
en_superman = False
index_frame = 0

# Variables pour l'animation
frame_delay = 0
delai_max_frame = 3

# Listes des obstacles
obstacles = []
obstacles_2 = []
obstacles_3 = []  # Liste pour le nouvel obstacle "suprise"

# Variables du jeu
horloge = pygame.time.Clock()
vitesse_jeu = 5  # Réduire la vitesse de jeu pour rendre le mouvement plus lent
gravite = 0.4  # Ajuster la gravité pour un saut plus fluide


# Paramètres de distance entre les obstacles
min_distance_entre_obstacles = 300
max_distance_entre_obstacles = 600

# Initialiser le score
score = 0

# Définir la police avant son utilisation
police = pygame.font.Font(None, 36)

# Charger l'image de fond pour l'écran Game Over (Mettre le chemin correct)
game_over_image = pygame.image.load('./src/games/gameDino/img/GameOver.png')
game_over_image = pygame.transform.scale(game_over_image, (400, 350))  # Redimensionner selon vos besoins

# Fonction pour dessiner le personnage
def afficher_personnage():
    global index_frame, frame_delay, en_superman
    frame_delay += 1

    if not en_superman:  # Animation de course normale
        if frame_delay >= delai_max_frame:
            index_frame = (index_frame + 1) % len(frames_personnage)
            frame_delay = 0
        ecran.blit(frames_personnage[index_frame], (x_personnage, y_personnage))
    else:
        # Position Superman
        ecran.blit(superman_image, (x_personnage, y_personnage))

# Fonctions pour créer de nouveaux obstacles
def creer_obstacle():
    if len(obstacles) == 0 or obstacles[-1][0] < LARGEUR - min_distance_entre_obstacles:
        distance_entre_obstacles = random.randint(min_distance_entre_obstacles, max_distance_entre_obstacles)
        obstacle_x = LARGEUR + distance_entre_obstacles
        obstacle_y = HAUTEUR - hauteur_obstacle
        obstacles.append([obstacle_x, obstacle_y])

def creer_obstacle_2():
    if len(obstacles_2) == 0 or obstacles_2[-1][0] < LARGEUR - min_distance_entre_obstacles:
        distance_entre_obstacles = random.randint(min_distance_entre_obstacles, max_distance_entre_obstacles)
        obstacle_x = LARGEUR + distance_entre_obstacles
        obstacle_y = HAUTEUR // 2
        obstacles_2.append([obstacle_x, obstacle_y])

def creer_obstacle_3():
    # Cet obstacle apparaîtra soudainement devant le personnage
    obstacle_x = x_personnage + random.randint(200, 400)
    obstacle_y = HAUTEUR - hauteur_obstacle
    obstacles_3.append([obstacle_x, obstacle_y])


# Contrôle de collision (obstacles au sol) - Basé sur des masques
def verifier_collision():
    if en_superman:
        personnage_image = superman_image
        personnage_mask = superman_mask
    else:
        personnage_image = frames_personnage[index_frame]
        personnage_mask = frames_personnage_masks[index_frame]

    personnage_rect = personnage_image.get_rect(topleft=(x_personnage, y_personnage))
    for obstacle in obstacles:
        obstacle_rect = image_obstacle.get_rect(topleft=(obstacle[0], obstacle[1]))
        if personnage_rect.colliderect(obstacle_rect):
            offset = (obstacle_rect.x - personnage_rect.x, obstacle_rect.y - personnage_rect.y)
            if personnage_mask.overlap(obstacle_mask, offset):
                return True
    return False

# Contrôle de collision (obstacles en hauteur) - Basé sur des masques
def verifier_collision_2():
    if en_superman:
        personnage_image = superman_image
        personnage_mask = superman_mask
    else:
        personnage_image = frames_personnage[index_frame]
        personnage_mask = frames_personnage_masks[index_frame]

    personnage_rect = personnage_image.get_rect(topleft=(x_personnage, y_personnage))
    for obstacle in obstacles_2:
        obstacle_rect = image_obstacle_2.get_rect(topleft=(obstacle[0], obstacle[1]))
        if personnage_rect.colliderect(obstacle_rect):
            offset = (obstacle_rect.x - personnage_rect.x, obstacle_rect.y - personnage_rect.y)
            if personnage_mask.overlap(obstacle_2_mask, offset):
                return True
    return False

# Contrôle de collision pour le nouvel obstacle
def verifier_collision_3():
    if en_superman:
        personnage_image = superman_image
        personnage_mask = superman_mask
    else:
        personnage_image = frames_personnage[index_frame]
        personnage_mask = frames_personnage_masks[index_frame]

    personnage_rect = personnage_image.get_rect(topleft=(x_personnage, y_personnage))
    for obstacle in obstacles_3:
        obstacle_rect = image_obstacle_3.get_rect(topleft=(obstacle[0], obstacle[1]))
        if personnage_rect.colliderect(obstacle_rect):
            offset = (obstacle_rect.x - personnage_rect.x, obstacle_rect.y - personnage_rect.y)
            if personnage_mask.overlap(obstacle_3_mask, offset):
                return True
    return False

# Fonctions pour dessiner les obstacles
def afficher_obstacle(obstacle_x, obstacle_y):
    ecran.blit(image_obstacle, (obstacle_x, obstacle_y))

def afficher_obstacle_2(obstacle_x, obstacle_y):
    ecran.blit(image_obstacle_2, (obstacle_x, obstacle_y))

def afficher_obstacle_3(obstacle_x, obstacle_y):
    ecran.blit(image_obstacle_3, (obstacle_x, obstacle_y))

# Fonction pour afficher le score
def afficher_score():
    texte_score = police.render(f"Score: {score}", True, NOIR)
    ecran.blit(texte_score, (LARGEUR - 150, 10))

# Fonction pour dessiner des rectangles avec coins arrondis (issue du premier code)
def dessiner_bouton_arrondi(ecran, couleur, rect, rayon):
    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(surface, couleur, (rayon, 0, rect.width - 2 * rayon, rect.height))  # Dessiner le rectangle principal
    pygame.draw.rect(surface, couleur, (0, rayon, rect.width, rect.height - 2 * rayon))
    pygame.draw.circle(surface, couleur, (rayon, rayon), rayon)  # Coin supérieur gauche
    pygame.draw.circle(surface, couleur, (rect.width - rayon, rayon), rayon)  # Coin supérieur droit
    pygame.draw.circle(surface, couleur, (rayon, rect.height - rayon), rayon)  # Coin inférieur gauche
    pygame.draw.circle(surface, couleur, (rect.width - rayon, rect.height - rayon), rayon)  # Coin inférieur droit
    ecran.blit(surface, rect.topleft)

# Fonction pour afficher l'écran de fin de jeu
def afficher_ecran_fin():
    ecran.fill(NOIR)
    
    # Afficher l'image de game over au centre de l'écran
    ecran.blit(game_over_image, ((LARGEUR - 300) // 2 - 60, (HAUTEUR - 300) // 3))  # Positionner l'image au centre

    # Créer deux boutons sous l'image
    bouton_rejouer = pygame.Rect((LARGEUR // 2) - 220, HAUTEUR // 2 + 100, 180, 50)  # Bouton Rejouer (à gauche)
    bouton_quitter = pygame.Rect((LARGEUR // 2) + 20, HAUTEUR // 2 + 100, 170, 50)   # Bouton Quitter (à droite)

    # Dessiner les boutons arrondis
    dessiner_bouton_arrondi(ecran, GRIS, bouton_rejouer, 20)  # Rayon des coins = 20
    dessiner_bouton_arrondi(ecran, ROUGE, bouton_quitter, 20)

    # Afficher les textes des boutons
    texte_rejouer = police.render("Rejouer", True, NOIR)
    texte_quitter = police.render("Quitter", True, BLANC)

    ecran.blit(texte_rejouer, (bouton_rejouer.x + 50, bouton_rejouer.y + 10))
    ecran.blit(texte_quitter, (bouton_quitter.x + 50, bouton_quitter.y + 10))

    pygame.display.flip()

    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_rejouer.collidepoint(event.pos):
                    reset_game()
                    en_cours = False
                if bouton_quitter.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Fonction pour réinitialiser le jeu
def reset_game():
    global x_personnage, y_personnage, vitesse_y, vitesse_x, sauter, en_superman, obstacles, obstacles_2, obstacles_3, score, vitesse_jeu
    x_personnage = 50
    y_personnage = HAUTEUR - hauteur_personnage
    vitesse_y = 0
    vitesse_x = 0
    sauter = False
    en_superman = False
    obstacles.clear()
    obstacles_2.clear()
    obstacles_3.clear()
    score = 0
    vitesse_jeu = 5  # Nous réinitialisons la vitesse du jeu
    boucle_jeu()

# Boucle principale du jeu
def boucle_jeu():
    global x_personnage, y_personnage, vitesse_y, vitesse_x, sauter, obstacles, obstacles_2, obstacles_3, en_superman, score, vitesse_jeu, gravite, index_frame

    en_cours = True
    horloge = pygame.time.Clock()
    temps_initial = pygame.time.get_ticks()

    while en_cours:
        # Mettre à jour le score et le temps
        temps_ecoule = pygame.time.get_ticks() - temps_initial
        score = temps_ecoule // 100

        # Augmenter la difficulté du jeu
        if score >= 200:
            background_color = GRIS3  # Mettre le fond en gris très foncé
            vitesse_jeu = 10          # Augmenter la vitesse du jeu
            gravite = 0.5             # Augmenter la gravité pour rendre le saut un peu plus difficile
            obstacle_chance = 15      # Augmenter la probabilité d'apparition des obstacles
        elif score >= 150:
            background_color = GRIS2  # Mettre le fond en gris foncé
            vitesse_jeu = 9
            gravite = 0.4
            obstacle_chance = 14
        elif score >= 100:
            background_color = GRIS   # Mettre le fond en gris clair
            vitesse_jeu = 8
            gravite = 0.4
            obstacle_chance = 12
        elif score >= 50:
            background_color = GRIS   # Mettre le fond en gris clair
            vitesse_jeu = 7
            gravite = 0.4
            obstacle_chance = 10
        else:
            background_color = BLANC  # Fond normal
            vitesse_jeu = 5
            gravite = 0.4
            obstacle_chance = 5

        ecran.fill(background_color)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not sauter and not en_superman:
                    vitesse_y = -10
                    sauter = True
                if event.key == pygame.K_SPACE and not sauter and not en_superman:
                    en_superman = True
                    vitesse_y = -8
                    vitesse_x = 3
                    sauter = True

        # Appliquer la gravité et le mouvement
        if sauter:
            vitesse_y += gravite
            y_personnage += vitesse_y
            x_personnage += vitesse_x

            # Le personnage revient lentement à la position de départ
            if not en_superman and x_personnage > 50:
                x_personnage -= 1

            # Réinitialiser les variables lorsque le personnage touche le sol
            if y_personnage >= HAUTEUR - hauteur_personnage:
                y_personnage = HAUTEUR - hauteur_personnage
                sauter = False
                vitesse_y = 0
                vitesse_x = 0
                en_superman = False

                # Reculer le personnage s'il est devant la position de départ
                if x_personnage > 50:
                    x_personnage -= 1

        # Si le personnage ne saute pas et est devant la position de départ, le reculer
        elif x_personnage > 50:
            x_personnage -= 1  # Le personnage recule lentement

        # Déplacer les obstacles
        for obstacle in obstacles:
            obstacle[0] -= vitesse_jeu

        for obstacle in obstacles_2:
            obstacle[0] -= vitesse_jeu

        for obstacle in obstacles_3:
            obstacle[0] -= vitesse_jeu  # Les bombes se déplacent maintenant vers le joueur

        # Supprimer les obstacles qui sortent de l'écran
        obstacles = [obstacle for obstacle in obstacles if obstacle[0] + largeur_obstacle > 0]
        obstacles_2 = [obstacle for obstacle in obstacles_2 if obstacle[0] + largeur_obstacle > 0]
        obstacles_3 = [obstacle for obstacle in obstacles_3 if obstacle[0] + largeur_obstacle > 0]

        # Créer des obstacles
        chance = random.randint(0, 100)
        if chance < obstacle_chance:
            creer_obstacle()

        if score > 100:
            chance = random.randint(0, 100)
            if chance < obstacle_chance:
                creer_obstacle_2()

        if score >= 250:
            # À des moments aléatoires, créer l'obstacle surprise
            chance = random.randint(0, 500)
            if chance < 5:  # Faible probabilité pour que l'obstacle apparaisse soudainement
                creer_obstacle_3()

        # Vérifier les collisions
        if verifier_collision() or verifier_collision_2() or verifier_collision_3():
            afficher_ecran_fin()
            en_cours = False
            continue

        # Afficher le personnage
        afficher_personnage()

        # Dessiner les obstacles
        for obstacle in obstacles:
            afficher_obstacle(obstacle[0], obstacle[1])

        for obstacle in obstacles_2:
            afficher_obstacle_2(obstacle[0], obstacle[1])

        for obstacle in obstacles_3:
            afficher_obstacle_3(obstacle[0], obstacle[1])

        # Afficher le score
        afficher_score()

        # Mettre à jour l'écran
        pygame.display.flip()
        horloge.tick(30)

    pygame.quit()
    sys.exit()

# Lancer le jeu
boucle_jeu()
