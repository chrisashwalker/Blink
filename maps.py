import random
from profiles import *

map_id = 0
drawn_map = None
drawn_map_entrance_rect = pygame.Rect(-64, -64, 0, 0)
drawn_map_exit_rect = pygame.Rect(-64, -64, 0, 0)
drawn_wall_rects = []
drawn_map_items_rects = []


# Creates and draws the map rects

class DrawMap:
    def __init__(self, map_layout, map_background, wall_img, map_music):
        self.map_background = map_background
        self.wall_img = wall_img
        self.map_music = map_music
        walls = []
        self.wall_rects = []
        map_items = []
        self.map_items_rects = []
        opponents_pos = []
        self.opponents = []
        o_id = -1
        map_lines = map_layout.splitlines()  # Splits the map multi-line string drawings into individual lines in a list
        self.map_entrance = None
        self.map_exit = None
        for line_index, each_line in enumerate(map_lines):  # assigns each value (each_line) a counter (line_index)
            for symbol_index, each_symbol in enumerate(
                    each_line):  # enumerate again working but with each character of each line instead
                if each_symbol == 'X':
                    walls.append((symbol_index, line_index))
                if each_symbol == 'A':
                    self.map_entrance = (symbol_index * tile_width, (line_index - 1) * tile_height)
                if each_symbol == 'B':
                    self.map_exit = (symbol_index * tile_width, (line_index - 1) * tile_height)
                if each_symbol == 'O':
                    opponents_pos.append((symbol_index, line_index))
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
        for o_pos in opponents_pos:
            random_op_no = random.randint(1, 3)
            o_id += 1
            self.opponents.append(Character('Enemy' + str(random_op_no), 5, 1, 5, -64, -64))
            self.opponents[o_id].rect.x = o_pos[0] * char_width
            self.opponents[o_id].rect.y = (o_pos[1] - 1) * char_height


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

map1 = DrawMap(map1_layout, bg3, wall1, track2)
map2 = DrawMap(map2_layout, bg3, wall1, track2)
map3 = DrawMap(map3_layout, bg3, wall1, track2)
map_tuple = (map1, map2, map3)


# Moving between maps

def map_change_check(player, current_map_id, current_map_entrance_rect, current_map_exit_rect):
    if current_map_entrance_rect.colliderect(hero.rect):
        new_map_id = current_map_id - 1
        player_x = 832
        player_y = current_map_entrance_rect[1]
    elif current_map_exit_rect.colliderect(hero.rect):
        new_map_id = current_map_id + 1
        player_x = 64
        player_y = current_map_exit_rect[1]
    else:
        new_map_id = current_map_id
        player_x = player.rect.x
        player_y = player.rect.y
    if map_tuple[current_map_id].map_music != map_tuple[new_map_id].map_music:
        soundtrack.stop()
        soundtrack.load(map_tuple[new_map_id].map_music)
        soundtrack.play(-1)
    new_opponents = map_tuple[new_map_id].opponents
    return int(new_map_id), player_x, player_y, list(new_opponents)
