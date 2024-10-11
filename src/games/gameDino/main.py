import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Running Game")

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
VERY_DARK_GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load character images (animations)
frame1 = pygame.image.load('./src/games/gameDino/img/h1.png').convert_alpha()
frame2 = pygame.image.load('./src/games/gameDino/img/h2.png').convert_alpha()
frame3 = pygame.image.load('./src/games/gameDino/img/h3.png').convert_alpha()
character_frames = [frame1, frame2, frame3]

# Créer les masques du personnage
''' Au lieu de rogner les images, la solution de ChatGPT 
    serait de rendre les arrière-plans transparents afin d'augmenter 
    la sensibilité de collision avec les obstacles. '''
frame1_mask = pygame.mask.from_surface(frame1)
frame2_mask = pygame.mask.from_surface(frame2)
frame3_mask = pygame.mask.from_surface(frame3)
character_frame_masks = [frame1_mask, frame2_mask, frame3_mask]

# Image and mask for Superman position
superman_image = pygame.image.load('./src/games/gameDino/img/h1-superMan.png').convert_alpha()
superman_mask = pygame.mask.from_surface(superman_image)

# Get character height
character_height = frame1.get_height()

# Load obstacle images
obstacle_image = pygame.image.load('./src/games/gameDino/img/obs1.png').convert_alpha()
obstacle_image_2 = pygame.image.load('./src/games/gameDino/img/obs2.png').convert_alpha()
obstacle_image_3 = pygame.image.load('./src/games/gameDino/img/obs3.png').convert_alpha()  # New obstacle

# Resize obstacle images
obstacle_width = 75
obstacle_height = 75
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))
obstacle_image_2 = pygame.transform.scale(obstacle_image_2, (obstacle_width, obstacle_height))
obstacle_image_3 = pygame.transform.scale(obstacle_image_3, (obstacle_width, obstacle_height))

# Recreate masks after resizing
obstacle_mask = pygame.mask.from_surface(obstacle_image)
obstacle_2_mask = pygame.mask.from_surface(obstacle_image_2)
obstacle_3_mask = pygame.mask.from_surface(obstacle_image_3)

# Initial character position
x_character = 50
y_character = HEIGHT - character_height  # Position the character on the ground
velocity_y = 0
velocity_x = 0  # Horizontal speed
jumping = False
in_superman_mode = False
frame_index = 0

# Variables for animation
frame_delay = 0
max_frame_delay = 3

# Lists of obstacles
obstacles = []
obstacles_2 = []
obstacles_3 = []  # List for the new "surprise" obstacle

# Game variables
clock = pygame.time.Clock()
game_speed = 5  # Reduce game speed for slower movement
gravity = 0.4  # Adjust gravity for smoother jumping

# Distance parameters between obstacles
min_distance_between_obstacles = 300
max_distance_between_obstacles = 600

# Initialize score
score = 0

# Définir la police avant son utilisation
police = pygame.font.Font(None, 36)


# Function to draw the character
def draw_character():
    global frame_index, frame_delay, in_superman_mode
    frame_delay += 1

    "formule chatGPT 'index_fame' "
    if not en_superman:  # Animation de course normale
        if frame_delay >= delai_max_frame:
            index_frame = (index_frame + 1) % len(frames_personnage)
            frame_delay = 0
        screen.blit(character_frames[frame_index], (x_character, y_character))
    else:
        # Superman position
        screen.blit(superman_image, (x_character, y_character))

# Fonctions pour créer de nouveaux obstacles
''''on evite les nouveaux obstacles d'apparaître à des endroits 
    impossibles en creant des valeurs min et max.'''
def creer_obstacle():
    if len(obstacles) == 0 or obstacles[-1][0] < LARGEUR - min_distance_entre_obstacles:
        distance_entre_obstacles = random.randint(min_distance_entre_obstacles, max_distance_entre_obstacles)
        obstacle_x = LARGEUR + distance_entre_obstacles
        obstacle_y = HAUTEUR - hauteur_obstacle
        obstacles.append([obstacle_x, obstacle_y])

def create_obstacle_2():
    if len(obstacles_2) == 0 or obstacles_2[-1][0] < WIDTH - min_distance_between_obstacles:
        distance_between_obstacles = random.randint(min_distance_between_obstacles, max_distance_between_obstacles)
        obstacle_x = WIDTH + distance_between_obstacles
        obstacle_y = HEIGHT // 2
        obstacles_2.append([obstacle_x, obstacle_y])

def create_obstacle_3():
    # This obstacle will suddenly appear in front of the character
    obstacle_x = x_character + random.randint(200, 400)
    obstacle_y = HEIGHT - obstacle_height
    obstacles_3.append([obstacle_x, obstacle_y])

# Contrôle de collision (obstacles au sol) - Basé sur des masques
def verifier_collision():
    if en_superman:
        personnage_image = superman_image
        personnage_mask = superman_mask
    else:
        character_image = character_frames[frame_index]
        character_mask = character_frame_masks[frame_index]

    character_rect = character_image.get_rect(topleft=(x_character, y_character))
    for obstacle in obstacles:
        obstacle_rect = obstacle_image.get_rect(topleft=(obstacle[0], obstacle[1]))
        if character_rect.colliderect(obstacle_rect):
            offset = (obstacle_rect.x - character_rect.x, obstacle_rect.y - character_rect.y)
            if character_mask.overlap(obstacle_mask, offset):
                return True
    return False

# Collision detection (high obstacles) - Based on masks
def check_collision_2():
    if in_superman_mode:
        character_image = superman_image
        character_mask = superman_mask
    else:
        character_image = character_frames[frame_index]
        character_mask = character_frame_masks[frame_index]

    character_rect = character_image.get_rect(topleft=(x_character, y_character))
    for obstacle in obstacles_2:
        obstacle_rect = obstacle_image_2.get_rect(topleft=(obstacle[0], obstacle[1]))
        if character_rect.colliderect(obstacle_rect):
            offset = (obstacle_rect.x - character_rect.x, obstacle_rect.y - character_rect.y)
            if character_mask.overlap(obstacle_2_mask, offset):
                return True
    return False

# Collision detection for the new obstacle
def check_collision_3():
    if in_superman_mode:
        character_image = superman_image
        character_mask = superman_mask
    else:
        character_image = character_frames[frame_index]
        character_mask = character_frame_masks[frame_index]

    character_rect = character_image.get_rect(topleft=(x_character, y_character))
    for obstacle in obstacles_3:
        obstacle_rect = obstacle_image_3.get_rect(topleft=(obstacle[0], obstacle[1]))
        if character_rect.colliderect(obstacle_rect):
            offset = (obstacle_rect.x - character_rect.x, obstacle_rect.y - character_rect.y)
            if character_mask.overlap(obstacle_3_mask, offset):
                return True
    return False

# Functions to draw obstacles
def draw_obstacle(obstacle_x, obstacle_y):
    screen.blit(obstacle_image, (obstacle_x, obstacle_y))

def draw_obstacle_2(obstacle_x, obstacle_y):
    screen.blit(obstacle_image_2, (obstacle_x, obstacle_y))

def draw_obstacle_3(obstacle_x, obstacle_y):
    screen.blit(obstacle_image_3, (obstacle_x, obstacle_y))

# Function to display the score
def display_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))

# Fonction pour afficher l'écran de fin de jeu
def afficher_ecran_fin():
    ecran.fill(BLANC)
    texte_fin = police.render("Game Over!", True, ROUGE)
    ecran.blit(texte_fin, (LARGEUR // 3, HAUTEUR // 3))

    bouton_rejouer = pygame.Rect(LARGEUR // 4, HAUTEUR // 2, 200, 50)
    bouton_quitter = pygame.Rect(LARGEUR // 2 + 100, HAUTEUR // 2, 200, 50)

    pygame.draw.rect(ecran, VERT, bouton_rejouer)
    pygame.draw.rect(ecran, ROUGE, bouton_quitter)

    texte_rejouer = police.render("Rejouer", True, NOIR)
    texte_quitter = police.render("Quitter", True, NOIR)

    screen.blit(replay_text, (replay_button.x + 50, replay_button.y + 10))
    screen.blit(quit_text, (quit_button.x + 50, quit_button.y + 10))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    reset_game()
                    running = False
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Function to reset the game
def reset_game():
    global x_character, y_character, velocity_y, velocity_x, jumping, in_superman_mode, obstacles, obstacles_2, obstacles_3, score, game_speed
    x_character = 50
    y_character = HEIGHT - character_height
    velocity_y = 0
    velocity_x = 0
    jumping = False
    in_superman_mode = False
    obstacles.clear()
    obstacles_2.clear()
    obstacles_3.clear()
    score = 0
    game_speed = 5  # Reset game speed
    game_loop()

# Main game loop
def game_loop():
    global x_character, y_character, velocity_y, velocity_x, jumping, obstacles, obstacles_2, obstacles_3, in_superman_mode, score, game_speed, gravity, frame_index

    running = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while running:
        # Update score and time
        elapsed_time = pygame.time.get_ticks() - start_time
        score = elapsed_time // 100

        # Augmenter la difficulté du jeu
        if score >= 400:
            background_color = GRIS3  # Mettre le fond en gris très foncé
            vitesse_jeu = 10          # Augmenter la vitesse du jeu
            gravite = 0.5             # Augmenter la gravité pour rendre le saut un peu plus difficile
            obstacle_chance = 15      # Augmenter la probabilité d'apparition des obstacles
        elif score >= 300:
            background_color = GRIS2  # Mettre le fond en gris foncé
            vitesse_jeu = 9
            gravite = 0.4
            obstacle_chance = 14
        elif score >= 200:
            background_color = GRIS   # Mettre le fond en gris clair
            vitesse_jeu = 8
            gravite = 0.4
            obstacle_chance = 12
        elif score >= 100:
            background_color = GRIS   # Mettre le fond en gris clair
            vitesse_jeu = 7
            gravite = 0.4
            obstacle_chance = 10
        else:
            background_color = WHITE           # Normal background
            game_speed = 5
            gravity = 0.4
            obstacle_chance = 5

        screen.fill(background_color)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not jumping and not in_superman_mode:
                    velocity_y = -10
                    jumping = True
                if event.key == pygame.K_SPACE and not jumping and not in_superman_mode:
                    in_superman_mode = True
                    velocity_y = -8
                    velocity_x = 3
                    jumping = True

        # Apply gravity and movement
        if jumping:
            velocity_y += gravity
            y_character += velocity_y
            x_character += velocity_x

            # Character slowly returns to starting position
            if not in_superman_mode and x_character > 50:
                x_character -= 1

            # Reset variables when character touches the ground
            if y_character >= HEIGHT - character_height:
                y_character = HEIGHT - character_height
                jumping = False
                velocity_y = 0
                velocity_x = 0
                in_superman_mode = False

                # Move character back if ahead of starting position
                if x_character > 50:
                    x_character -= 1

        # If character is not jumping and is ahead of starting position, move back
        elif x_character > 50:
            x_character -= 1  # Character moves back slowly

        # Move obstacles
        for obstacle in obstacles:
            obstacle[0] -= game_speed

        for obstacle in obstacles_2:
            obstacle[0] -= game_speed

        for obstacle in obstacles_3:
            obstacle[0] -= game_speed  # Bombs now move towards the player

        # Remove obstacles that go off screen
        obstacles = [obstacle for obstacle in obstacles if obstacle[0] + obstacle_width > 0]
        obstacles_2 = [obstacle for obstacle in obstacles_2 if obstacle[0] + obstacle_width > 0]
        obstacles_3 = [obstacle for obstacle in obstacles_3 if obstacle[0] + obstacle_width > 0]

        # Create obstacles
        chance = random.randint(0, 100)
        if chance < obstacle_chance:
            create_obstacle()

        if score > 100:
            chance = random.randint(0, 100)
            if chance < obstacle_chance:
                create_obstacle_2()

        if score >= 400:
            # À des moments aléatoires, créer l'obstacle surprise
            chance = random.randint(0, 500)
            if chance < 5:  # Low probability for the obstacle to suddenly appear
                create_obstacle_3()

        # Check collisions
        if check_collision() or check_collision_2() or check_collision_3():
            display_game_over_screen()
            running = False
            continue

        # Draw the character
        draw_character()

        # Draw obstacles
        for obstacle in obstacles:
            draw_obstacle(obstacle[0], obstacle[1])

        for obstacle in obstacles_2:
            draw_obstacle_2(obstacle[0], obstacle[1])

        for obstacle in obstacles_3:
            draw_obstacle_3(obstacle[0], obstacle[1])

        # Display the score
        display_score()

        # Update the screen
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

# Start the game
game_loop()
