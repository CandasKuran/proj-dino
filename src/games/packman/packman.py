import pygame

pygame.init()

# Set up the drawing window
WIDTH = 950
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
fps = 60
timer = pygame.time.Clock()
packman_font = "assets/Emulogic-zrEw.ttf"
font = pygame.font.Font(packman_font, 20)


# Run until the user asks to quit
running = True

while running:
    timer.tick(fps)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update the display 
    pygame.display.flip()
    
# Done! Time to quit.
pygame.quit()

