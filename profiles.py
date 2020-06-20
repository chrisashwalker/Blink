import pygame
pygame.init()
import os
from shared import *

# Character object
	# name
	# base health points
	# base ability points
	# strength
	# boosted strength
	# restoration power
	# position x coordinate
	# position y coordinate
	# image width constant
	# image height constant
	# movement speed
	
class character:
	def __init__(char, name, base_hp, base_ap, st , bst, rest, speed, x, y):
		char.name = name
		char.base_hp = base_hp
		char.base_ap = base_ap
		char.st = st
		char.bst = bst
		char.rest = rest
		char.speed = speed
		char.x = x
		char.y = y
		char.width = char_width
		char.height = char_height
		char.img = os.path.join('images', (char.name + '.png'))
	
	def load_img(char):
		return pygame.image.load(char.img).convert_alpha()

# Character declarations

hero = character('Hero', 10, 5, 2, 4, 1, 10, 0, 0)
enemy1 = character('Enemy1', 5, 5, 1, 2, 0, 5, -64, -64)
