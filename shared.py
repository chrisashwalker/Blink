import os
import pygame

pygame.init()

# Window settings, shared variables, pygame surfaces and sounds
window_width = 960
window_height = 640
window = pygame.display.set_mode((window_width, window_height))
title = pygame.display.set_caption('Blink')
framerate = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
bigtext = pygame.font.SysFont('Arial', 50)
text = pygame.font.SysFont('Arial', 20)
tile_width = 64
tile_height = 64
char_width = 64
char_height = 64

# TODO: Consider cutting down on no. of surfaces
saves_surface = pygame.Surface((800, 400))
intro_surface = pygame.Surface((960, 640))
intro_surface.fill((0, 0, 0))
blink_surface = pygame.Surface((960, 640))
blink_surface.fill((0, 0, 0))
blink_surface.set_alpha(0)
trans_surface = pygame.Surface((960, 640))
trans_surface.set_alpha(0)
msg_surface = pygame.Surface((800, 400))
wall_surface = pygame.Surface((64, 64))
items_surface = pygame.Surface((64, 64))

soundtrack = pygame.mixer.music
soundtrack.set_volume(0.9)
track1 = os.path.join('sounds', 'track1.wav')
track2 = os.path.join('sounds', 'track2.wav')
track3 = os.path.join('sounds', 'track3.wav')
hit = pygame.mixer.Sound(os.path.join('sounds', 'hit.wav'))
siren = pygame.mixer.Sound(os.path.join('sounds', 'siren.wav'))
