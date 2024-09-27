import pygame

def charger_personnage():
    # Charger les frames du personnage en mouvement
    personnage_frames = [
        pygame.image.load('./src/games/monster-run/images/h1.png'),
        pygame.image.load('./src/games/monster-run/images/h2.png'),
        pygame.image.load('./src/games/monster-run/images/h3.png'),
        pygame.image.load('./src/games/monster-run/images/h4.png')
    ]
    # Redimensionner les frames si nécessaire
    personnage_frames = [pygame.transform.scale(frame, (75, 75)) for frame in personnage_frames]
    return personnage_frames

def afficher_personnage_animate(ecran, frames, index_frame, carre_x, carre_y):
    # Dessiner l'image animée du personnage
    ecran.blit(frames[index_frame], (carre_x, carre_y))

def mettre_a_jour_animation(index_frame, temps_animation, intervalle_animation, horloge, frames):
    # Gérer l'animation du personnagea
    temps_animation += horloge.get_time()
    if temps_animation > intervalle_animation:
        index_frame = (index_frame + 1) % len(frames)  # Passer à la frame suivante
        temps_animation = 0
    return index_frame, temps_animation
