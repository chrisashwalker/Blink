import os
import pygame

pygame.init()

# Window settings, shared variables, pygame surfaces and sounds
title = 'Blink'
window_width = 960
window_height = 640
window = pygame.display.set_mode((window_width, window_height))
title = pygame.display.set_caption(title)
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
intro_surface = pygame.Surface((window_width, window_height))
intro_surface.fill((0, 0, 0))
blink_surface = pygame.Surface((window_width, window_height))
blink_surface.fill((0, 0, 0))
blink_surface.set_alpha(0)
trans_surface = pygame.Surface((window_width, window_height))
trans_surface.set_alpha(0)
msg_surface = pygame.Surface((800, 400))
wall_surface = pygame.Surface((tile_width, tile_height))

sound_folder = 'sounds'
soundtrack = pygame.mixer.music
soundtrack.set_volume(0.9)
track1 = os.path.join(sound_folder, 'track1.wav')
track2 = os.path.join(sound_folder, 'track2.wav')
track3 = os.path.join(sound_folder, 'track3.wav')
hit = pygame.mixer.Sound(os.path.join(sound_folder, 'hit.wav'))
siren = pygame.mixer.Sound(os.path.join(sound_folder, 'siren.wav'))

graphics_folder = 'graphics'
