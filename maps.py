import pygame
pygame.init()
from shared import *
from profiles import *

map_ID = 0
drawn_map = None
drawn_map_entrance_rect = pygame.Rect(-64, -64, 0, 0)
drawn_map_exit_rect = pygame.Rect(-64, -64, 0, 0)
drawn_wall_rects = list() 
drawn_opponents_rects = list()
drawn_map_items_rects = list()

# Creates and draws the map rects

class draw_map:
	def __init__(self, map_layout, map_background, wall_img, map_music):
		self.map_background = map_background
		self.wall_img = wall_img
		self.map_music = map_music
		walls = []
		self.wall_rects = []
		map_items = []
		self.map_items_rects = []
		opponents = []
		self.opponents_rects = []
		map_lines = map_layout.splitlines() # Splits the map multi-line string drawings into individual lines in a list
		self.map_entrance = None
		self.map_exit = None
		for line_index, each_line in enumerate(map_lines): # enumerate() is working through the map_lines list, assigning each value (each_line) a unique counter (line_index)
			for symbol_index, each_symbol in enumerate(each_line): # enumerate again working but with each character of each line instead
				if each_symbol == 'X':
					walls.append((symbol_index, line_index))
				if each_symbol == 'A':
					self.map_entrance = (symbol_index * tile_width, (line_index - 1) * tile_height)
				if each_symbol == 'B':
					self.map_exit = (symbol_index * tile_width, (line_index - 1) * tile_height)
				if each_symbol == 'O':
					opponents.append((symbol_index, line_index))
				if each_symbol == 'I':
					map_items.append((symbol_index, line_index))
		# Loop through the lists of walls and opponents to create their rects for pygame
		for wall in walls:
			wall_x = wall[0] * tile_width
			wall_y = (wall[1] - 1) * tile_height
			wall_width = tile_width
			wall_height = tile_height
			self.wall_rects.append(pygame.Rect(wall_x, wall_y, wall_width, wall_height))
		for map_item in map_items:
			map_item_x = map_item[0] * tile_width
			map_item_y = (map_item[1] - 1) * tile_height
			map_item_width = tile_width
			map_item_height = tile_height
			self.map_items_rects.append(pygame.Rect(map_item_x, map_item_y, map_item_width, map_item_height))
		for opponent in opponents:
			opponent_x = opponent[0] * char_width
			opponent_y = (opponent[1] - 1) * char_height
			opponent_width = char_width
			opponent_height = char_height
			self.opponents_rects.append(pygame.Rect(opponent_x, opponent_y, opponent_width, opponent_height))

bg1 = pygame.image.load(os.path.join('images', 'bg1.png')).convert_alpha()
bg2 = pygame.image.load(os.path.join('images', 'bg2.png')).convert_alpha()
bg3 = pygame.image.load(os.path.join('images', 'bg3.png')).convert_alpha()

wall1 = pygame.image.load(os.path.join('images', 'wall.png')).convert_alpha()

# Map layouts; 'A' symbol is the entrance, 'B' is the exit, 'I' are items, 'O' are opponents and 'X' are walls

map1_layout = '''
.X.............
.X......X......
........X......
XXXXX........O.
...............
...............
.X.....X.......
.X.....XXXXX...
..........XXXXX
..............B
'''

map2_layout = '''
..IX...........
..XX.......O...
..............B
.......XXXX....
...............
..............X
...O..........X
..............X
XXXX..........X
A.............X
'''

map3_layout = '''
.....XXXX......
...............
A..............
.....X......X..
.....X......XI.
.....X......XXX
...............
..XXX..........
..........O....
...O...........
'''
map1 = draw_map(map1_layout, bg3, wall1, track1)
map2 = draw_map(map2_layout, bg3, wall1, track1)
map3 = draw_map(map3_layout, bg3, wall1, track1)
map_tuple = (map1, map2, map3)

# Moving between maps
def map_change_check(window, hero, map_ID, drawn_map, drawn_map_entrance_rect, drawn_map_exit_rect, wall_surface, found_items_rects, new_map_data):
	if drawn_map_entrance_rect.collidepoint((int(hero.x + (hero.width / 2)), int(hero.y + (hero.height / 2)))) == True:
		current_map_music = drawn_map.map_music
		map_ID -= 1
		hero.x = 832
		hero.y = drawn_map_entrance_rect[1]
		window.blit(map_tuple[map_ID].map_background, (0, 0))
		window.blit(hero.load_img(), (hero.x, hero.y))
		drawn_map = map_tuple[map_ID]
		drawn_wall_rects = drawn_map.wall_rects
		drawn_map_entrance = drawn_map.map_entrance
		drawn_map_exit = drawn_map.map_exit
		if drawn_map.map_music != current_map_music:
			soundtrack.load(drawn_map.map_music)
			#soundtrack.play(-1)
		if drawn_map_entrance == None:
			drawn_map_entrance_rect = pygame.Rect(-64, -64, 0, 0)
		else:
			drawn_map_entrance_rect = pygame.Rect(drawn_map_entrance[0], drawn_map_entrance[1], 64, 64)
		if drawn_map_exit == None:
			drawn_map_exit_rect = pygame.Rect(-64, -64, 0, 0)
		else:
			drawn_map_exit_rect = pygame.Rect(drawn_map_exit[0], drawn_map_exit[1], 64, 64)
		window.blit(entrance_img, drawn_map_entrance_rect)
		window.blit(exit_img, drawn_map_exit_rect)
		wall_surface.blit(wall1, (0, 0))
		for w_rect in drawn_wall_rects:
			window.blit(wall_surface, w_rect)
		drawn_opponents_rects = drawn_map.opponents_rects
		for o_rect in drawn_opponents_rects:
			window.blit(enemy1.load_img(), (o_rect[0], o_rect[1]))
		drawn_map_items_rects = drawn_map.map_items_rects
		for i_rect in drawn_map_items_rects:
			if i_rect not in found_items_rects:
				window.blit(item_img, i_rect)
		pygame.display.flip()
		new_map_data = (map_ID, drawn_map, drawn_map_entrance_rect, drawn_map_exit_rect, drawn_wall_rects, drawn_opponents_rects, drawn_map_items_rects)
		return new_map_data
		
	elif drawn_map_exit_rect.collidepoint((int(hero.x + (hero.width / 2)), int(hero.y + (hero.height / 2)))) == True:
		current_map_music = drawn_map.map_music
		map_ID += 1
		hero.x = 64
		hero.y = drawn_map_exit_rect[1]
		window.blit(map_tuple[map_ID].map_background, (0, 0))
		window.blit(hero.load_img(), (hero.x, hero.y))
		drawn_map = map_tuple[map_ID]
		drawn_wall_rects = drawn_map.wall_rects
		drawn_map_entrance = drawn_map.map_entrance
		drawn_map_exit = drawn_map.map_exit
		if drawn_map.map_music != current_map_music:
			soundtrack.load(drawn_map.map_music)
			#soundtrack.play(-1)
		if drawn_map_entrance == None:
			drawn_map_entrance_rect = pygame.Rect(-64, -64, 0, 0)
		else:
			drawn_map_entrance_rect = pygame.Rect(drawn_map_entrance[0], drawn_map_entrance[1], 64, 64)
		if drawn_map_exit == None:
			drawn_map_exit_rect = pygame.Rect(-64, -64, 0, 0)
		else:
			drawn_map_exit_rect = pygame.Rect(drawn_map_exit[0], drawn_map_exit[1], 64, 64)
		window.blit(entrance_img, drawn_map_entrance_rect)
		window.blit(exit_img, drawn_map_exit_rect)
		wall_surface.blit(wall1, (0, 0))
		for w_rect in drawn_wall_rects:
			window.blit(wall_surface, w_rect)
		drawn_opponents_rects = drawn_map.opponents_rects
		for o_rect in drawn_opponents_rects:
			window.blit(enemy1.load_img(), (o_rect[0], o_rect[1]))
		drawn_map_items_rects = drawn_map.map_items_rects
		for i_rect in drawn_map_items_rects:
			if i_rect not in found_items_rects:
				window.blit(item_img, i_rect)
		pygame.display.flip()
		new_map_data = (map_ID, drawn_map, drawn_map_entrance_rect, drawn_map_exit_rect, drawn_wall_rects, drawn_opponents_rects, drawn_map_items_rects)
		return new_map_data
	else:
		return new_map_data
		