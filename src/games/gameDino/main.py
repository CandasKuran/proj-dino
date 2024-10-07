import pygame
import random

# Initialiser Pygame
pygame.init()

# Dimensions de l'écran
LARGEUR, HAUTEUR = 1200, 600
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu de course ")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Charger les images du personnage (animations)
frame1 = pygame.image.load('./src/games/gameDino/img/h1.png')
frame2 = pygame.image.load('./src/games/gameDino/img/h2.png')
frame3 = pygame.image.load('./src/games/gameDino/img/h3.png')
frames_personnage = [frame1, frame2, frame3]

# Position initiale du personnage
x_personnage = 50
y_personnage = HAUTEUR - 150  # Ajuster la position pour bien voir le personnage
vitesse_y = 0
sauter = False
index_frame = 0

# Variables pour l'animation
frame_delay = 0  # Compteur pour ralentir l'animation
delai_max_frame = 3  # Ajuster cette valeur pour ralentir l'animation (plus grand = plus lent)

# Liste des obstacles
obstacles = []

# Variables de jeu
horloge = pygame.time.Clock()
vitesse_jeu = 9  # Réduire la vitesse de jeu pour rendre le mouvement plus lent
gravite = 0.4  # Ajuster la gravité pour un saut plus fluide

# Fonction pour dessiner le personnage
def afficher_personnage():
    global index_frame, frame_delay
    frame_delay += 1

    if frame_delay >= delai_max_frame:  # Attendre avant de changer de frame
        index_frame = (index_frame + 1) % len(frames_personnage)
        frame_delay = 0  # Réinitialiser le compteur après le changement de frame

    ecran.blit(frames_personnage[index_frame], (x_personnage, y_personnage))

# Fonction pour créer un nouvel obstacle
def creer_obstacle():
    obstacle_x = LARGEUR
    obstacle_y = HAUTEUR - 50  # Ajuster la hauteur pour que l'obstacle soit bien visible
    obstacles.append([obstacle_x, obstacle_y])

# Fonction pour vérifier si on touche un obstacle
def verifier_collision():
    for obstacle in obstacles:
        if x_personnage + 50 > obstacle[0] and y_personnage + 50 > obstacle[1]:
            return True
    return False

# Boucle principale du jeu
def boucle_jeu():
    global y_personnage, vitesse_y, sauter, obstacles

    en_cours = True
    while en_cours:
        ecran.fill(BLANC)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not sauter:
                        vitesse_y = -10  # Sauter
                        sauter = True

        # Appliquer la gravité
        vitesse_y = vitesse_y + gravite
        y_personnage = y_personnage + vitesse_y

        # Empêcher le personnage de tomber
        if y_personnage > HAUTEUR - 150:
            y_personnage = HAUTEUR - 150
            sauter = False

        # Déplacer les obstacles
        for obstacle in obstacles:
            obstacle[0] = obstacle[0] - vitesse_jeu
        
        nouveaux_obstacles = []
        for obstacle in obstacles:
            if obstacle[0] > 0:
                nouveaux_obstacles.append(obstacle)
        obstacles = nouveaux_obstacles

        # Créer un nouvel obstacle de temps en temps
        if random.randint(0, 100) < 5:
            creer_obstacle()

        # Vérifier la collision
        if verifier_collision():
            print("Collision ! Game Over")
            en_cours = False

        # Afficher le personnage
        afficher_personnage()

        # Dessiner les obstacles
        for obstacle in obstacles:
            pygame.draw.rect(ecran, ROUGE, (obstacle[0], obstacle[1], 50, 50))

        # Mettre à jour l'écran
        pygame.display.flip()
        horloge.tick(30)

# Lancer le jeu
boucle_jeu()

# Quitter Pygame
pygame.quit()
