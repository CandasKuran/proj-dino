import pygame

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
largeur = 800
hauteur = 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu du Moulin")

# Boucle principale du jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran
    fenetre.fill((255, 255, 255))

    # Dessiner le plateau de jeu
    pygame.draw.line(fenetre, (0, 0, 0), (100, 100), (700, 100), 5)
    pygame.draw.line(fenetre, (0, 0, 0), (100, 300), (700, 300), 5)
    pygame.draw.line(fenetre, (0, 0, 0), (100, 500), (700, 500), 5)
    pygame.draw.line(fenetre, (0, 0, 0), (100, 100), (100, 500), 5)
    pygame.draw.line(fenetre, (0, 0, 0), (300, 100), (300, 500), 5)
    pygame.draw.line(fenetre, (0, 0, 0), (500, 100), (500, 500), 5)
    pygame.draw.line(fenetre, (0, 0, 0), (700, 100), (700, 500), 5)
    pygame.draw.circle(fenetre, (0, 0, 0), (100, 100), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (300, 100), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (500, 100), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (700, 100), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (100, 300), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (300, 300), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (500, 300), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (700, 300), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (100, 500), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (300, 500), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (500, 500), 10)
    pygame.draw.circle(fenetre, (0, 0, 0), (700, 500), 10)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()