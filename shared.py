import os

import pygame

pygame.init()

# Window settings, shared variables, backgrounds and music
window_width = 960
window_height = 640
window = pygame.display.set_mode((window_width, window_height))
title = pygame.display.set_caption('Untitled Game')
framerate = pygame.time.Clock()
bigtext = pygame.font.SysFont('Arial', 50)
text = pygame.font.SysFont('Arial', 20)
tile_width = 64
tile_height = 64
char_width = 64
char_height = 64
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
msg_surface = pygame.Surface((800, 300))
wall_surface = pygame.Surface((64, 64))
items_surface = pygame.Surface((64, 64))
item_img = pygame.image.load(os.path.join('images', 'item.png')).convert_alpha()
entrance_img = pygame.image.load(os.path.join('images', 'entrance.png')).convert_alpha()
exit_img = pygame.image.load(os.path.join('images', 'exit.png')).convert_alpha()
soundtrack = pygame.mixer.music
track1 = os.path.join('music', 'track1.wav')
