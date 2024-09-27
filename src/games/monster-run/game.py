import pygame
import sys
import time
import random

from mainChar import charger_personnage, afficher_personnage_animate, mettre_a_jour_animation
from globals import selected_character, player_name
from mainChar import charger_personnage as charger_personnage1
from char2 import charger_personnage as charger_personnage2
from char3 import charger_personnage as charger_personnage3

# Initialiser Pygame
pygame.init()

# Dimensions de l'écran
LARGEUR, HAUTEUR = 1200, 800

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
GRIS = (192, 192, 192)  # #c0c0c0 en format RGB
BLACK = (26, 28, 27)
OVER = (246, 246, 246, 255) 


try:
    # Charger les frames du personnage en mouvement
    frames = charger_personnage()
    # Charger l'image de fond 
    background_image = pygame.image.load('./src/games/monster-run/images/MainBg.png')
    background_image = pygame.transform.scale(background_image, (LARGEUR, HAUTEUR))
except pygame.error as e:
    print(f"Erreur lors du chargement des images: {e}")
    pygame.quit()
    sys.exit()

# Charger l'image de fond pour l'écran Game Over (Mettre le chemin correct)
game_over_image = pygame.image.load('./src/games/monster-run/images/GameOver1.png')
game_over_image = pygame.transform.scale(game_over_image, (400, 350))  # Redimensionner selon vos besoins

# Index de l'animation du personnage
index_frame = 0
temps_animation = 0  # Temps écoulé pour changer la frame
intervalle_animation = 100  # Intervalle entre les frames (en millisecondes)

# Dimensions des obstacles
LARGEUR_OBSTACLE = 50
HAUTEUR_OBSTACLE = 50

# Créer la fenêtre du jeu
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu Principal")

# Position initiale du personnage
carre_x = LARGEUR // 4
carre_y = HAUTEUR // 2

# Vitesse de déplacement
vitesse_x = 0
vitesse_y = 0

# Liste des obstacles
obstacles = []

# Horloge du jeu pour contrôler la vitesse du jeu
horloge = pygame.time.Clock()

# Police pour le texte
police = pygame.font.SysFont(None, 55)

# Variables pour le niveau et le temps
niveau = 1
temps_niveau = 5  # Chaque niveau dure 5 secondes
temps_initial = time.time()
vitesse_obstacles = 2  # Vitesse initiale des obstacles

background_x = 0

def afficher_message(texte, couleur, x, y):
    police = pygame.font.SysFont("arial", 30)  # Police d'écriture
    texte_surface = police.render(texte, True, couleur)
    ecran.blit(texte_surface, (x, y))  # Dessine le texte à la position (x, y)


# Fonction pour afficher la durée et le niveau en haut à droite
def afficher_temps_et_niveau(temps_restant, niveau):
    temps_texte = f"Temps: {temps_restant:.0f} sec"
    niveau_texte = f"Niveau: {niveau}"
    afficher_message(temps_texte, NOIR, LARGEUR - 250, 10)
    afficher_message(niveau_texte, NOIR, LARGEUR - 250, 50)

# Fonction pour créer un nouvel obstacle
def creer_obstacle():
    obstacle_x = LARGEUR
    obstacle_y = random.randint(0, HAUTEUR - HAUTEUR_OBSTACLE)
    obstacles.append([obstacle_x, obstacle_y])

# Fonction pour vérifier les collisions
def verifier_collision(carre_rect, objets):
    for objet in objets:
        objet_rect = pygame.Rect(objet[0], objet[1], LARGEUR_OBSTACLE, HAUTEUR_OBSTACLE)
        if carre_rect.colliderect(objet_rect):
            print(f"Collision détectée avec un obstacle à la position: {objet[0]}, {objet[1]}")  # Debugging pour les collisions
            return True
    return False


# Fonction pour dessiner des rectangles avec coins arrondis
def dessiner_bouton_arrondi(ecran, couleur, rect, rayon):
    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(surface, couleur, (rayon, 0, rect.width - 2 * rayon, rect.height))  # Dessiner le rectangle principal
    pygame.draw.rect(surface, couleur, (0, rayon, rect.width, rect.height - 2 * rayon))
    pygame.draw.circle(surface, couleur, (rayon, rayon), rayon)  # Coin supérieur gauche
    pygame.draw.circle(surface, couleur, (rect.width - rayon, rayon), rayon)  # Coin supérieur droit
    pygame.draw.circle(surface, couleur, (rayon, rect.height - rayon), rayon)  # Coin inférieur gauche
    pygame.draw.circle(surface, couleur, (rect.width - rayon, rect.height - rayon), rayon)  # Coin inférieur droit
    ecran.blit(surface, rect.topleft)


def afficher_ecran_game_over():
    ecran.fill(BLACK)  # Remplir le fond avec une couleur
    
    # Afficher l'image de game over au centre de l'écran
    ecran.blit(game_over_image, ((LARGEUR - 300) // 2 - 60, (HAUTEUR - 300) // 3))  # Positionner l'image au centre
    
    # Créer deux boutons sous l'image
    bouton_rejouer = pygame.Rect((LARGEUR // 2) - 220, HAUTEUR // 2 + 100, 180, 50)  # Bouton Rejouer (à gauche)
    bouton_quitter = pygame.Rect((LARGEUR // 2) + 20, HAUTEUR // 2 + 100, 170, 50)   # Bouton Quitter (à droite)
    
    # Dessiner les boutons arrondis
    dessiner_bouton_arrondi(ecran, GRIS, bouton_rejouer, 20)  # Rayon des coins = 20
    dessiner_bouton_arrondi(ecran, ROUGE, bouton_quitter, 20)
    
    # Afficher les textes des boutons
    afficher_message("Rejouer", NOIR, (LARGEUR // 2) - 200, HAUTEUR // 2 + 110)
    afficher_message("Quitter", BLANC, (LARGEUR // 2) + 40, HAUTEUR // 2 + 110)
    
    pygame.display.flip()

    # Boucle pour gérer les événements
    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_rejouer.collidepoint(evenement.pos):
                    game_loop()  # Relancer la fonction principale du jeu
                if bouton_quitter.collidepoint(evenement.pos):
                    pygame.quit()
                    sys.exit()

# Fonction principale du jeu
def game_loop():
    from boss1 import boss1_loop
    from boss2 import boss2_loop
    from boss3 import boss3_loop
    from boss4 import boss4_loop
    from boss5 import boss5_loop
    from bossfinal import final_boss_loop
    from globals import selected_character, player_name  # Global variables are imported from globals.py


    global carre_x, carre_y, obstacles, vitesse_x, vitesse_y, niveau, vitesse_obstacles, temps_initial, index_frame, temps_animation, background_x

        # Sélectionner l'animation du personnage selon le choix
    if selected_character == 0:
        frames = charger_personnage1()  # Main character
    elif selected_character == 1:
        frames = charger_personnage2()  # Deuxième personnage
    elif selected_character == 2:
        frames = charger_personnage3()  # Troisième personnage
    else:
        # Si aucun personnage n'est sélectionné, charger un personnage par défaut
        frames = charger_personnage1()  # Par défaut, on charge le premier personnage

     # Afficher le nom du joueur en haut
    afficher_message(f"Joueur: {player_name}", NOIR, 10, 10)

    # Réinitialiser les variables de jeu
    carre_x = LARGEUR // 4
    carre_y = HAUTEUR // 2
    vitesse_x = 0
    vitesse_y = 0
    obstacles = []
    niveau = 1
    vitesse_obstacles = 12
    temps_initial = time.time()

    while True:
        # Mode normal pendant 5 secondes
        temps_courant = time.time()
        temps_ecoule = temps_courant - temps_initial

        # Mettre à jour l'animation du personnage
        index_frame, temps_animation = mettre_a_jour_animation(index_frame, temps_animation, intervalle_animation, horloge, frames)

        if temps_ecoule > 2:
            print(f"Transition vers le boss {niveau}")  # Debugging pour les bosses
            niveau += 1
            temps_initial = time.time()
            obstacles = []

            try:
                # Appeler le boss correspondant
                if niveau == 2:
                    if not boss1_loop():
                        print("Boss 1 terminé ou échoué.")  # Debugging pour Boss 1
                        afficher_ecran_game_over()
                        return
                elif niveau == 3:
                    if not boss2_loop():
                        print("Boss 2 terminé ou échoué.")  # Debugging pour Boss 2
                        afficher_ecran_game_over()
                        return
                elif niveau == 4:
                    if not boss3_loop():
                        print("Boss 3 terminé ou échoué.")  # Debugging pour Boss 3
                        afficher_ecran_game_over()
                        return
                elif niveau == 5:
                    if not boss4_loop():
                        print("Boss 4 terminé ou échoué.")  # Debugging pour Boss 4
                        afficher_ecran_game_over()
                        return
                elif niveau == 6:
                    if not boss5_loop():
                        print("Boss 5 terminé ou échoué.")  # Debugging pour Boss 5
                        afficher_ecran_game_over()
                        return
                elif niveau == 7:
                    if not final_boss_loop():
                        print("Final Boss terminé ou échoué.")  # Debugging pour Final Boss
                        afficher_ecran_game_over()
                        return
            except Exception as e:
                print(f"Erreur pendant le boss {niveau}: {e}")
                afficher_ecran_game_over()
                return

            # Réinitialiser le temps après le boss
            temps_initial = time.time()

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

        carre_x = max(0, min(carre_x, LARGEUR - frames[0].get_width()))  # Limiter le mouvement dans l'écran
        carre_y = max(0, min(carre_y, HAUTEUR - frames[0].get_height()))

        if random.randint(0, 100) < 8:
            creer_obstacle()

        for obstacle in obstacles:
            obstacle[0] -= vitesse_obstacles

        obstacles = [obstacle for obstacle in obstacles if obstacle[0] > -LARGEUR_OBSTACLE]

        carre_rect = pygame.Rect(carre_x, carre_y, frames[0].get_width(), frames[0].get_height())
        if verifier_collision(carre_rect, obstacles):
            afficher_ecran_game_over()
            return

        # glisser l'ecran a gauche
        background_x -= 5  # vitesse 

        #
        ecran.blit(background_image, (background_x, 0))
        ecran.blit(background_image, (background_x + LARGEUR, 0)) 

        # effet boucle
        if background_x <= -LARGEUR:
            background_x = 0

        # Dessiner l'image animée du personnage
        afficher_personnage_animate(ecran, frames, index_frame, carre_x, carre_y)

        for obstacle in obstacles:
            pygame.draw.rect(ecran, ROUGE, (obstacle[0], obstacle[1], LARGEUR_OBSTACLE, HAUTEUR_OBSTACLE))

        temps_restant = 10 - temps_ecoule
        afficher_temps_et_niveau(temps_restant, niveau)

        pygame.display.flip()

        horloge.tick(60)

# Lancer le jeu
if __name__ == "__main__":
    try:
        game_loop()
    except Exception as e:
        print(f"Erreur: {e}")
        pygame.quit()
        sys.exit()
