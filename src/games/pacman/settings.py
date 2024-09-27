import pygame as pg
from board import boards
import copy
import math

# Window settings
WIDTH = 900
HEIGHT = 950

screen = pg.display.set_mode((WIDTH, HEIGHT))
timer = pg.time.Clock()
fps = 60
level = copy.deepcopy(boards[0])
color = 'blue'

PI = math.pi

player_images = [] # This is a list of images for the player

for i 