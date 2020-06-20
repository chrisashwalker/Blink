from profiles import *

pygame.init()

map_ID = 0
drawn_map = None
drawn_map_entrance_rect = pygame.Rect(-64, -64, 0, 0)
drawn_map_exit_rect = pygame.Rect(-64, -64, 0, 0)
drawn_wall_rects = list()
drawn_opponents_rects = list()
drawn_map_items_rects = list()


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
        opponents = []
        self.opponents_rects = []
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

map1 = DrawMap(map1_layout, bg3, wall1, track1)
map2 = DrawMap(map2_layout, bg3, wall1, track1)
map3 = DrawMap(map3_layout, bg3, wall1, track1)
map_tuple = (map1, map2, map3)


# Moving between maps
def map_change_check(surface, player, map_id, current_map, current_map_entrance_rect, current_map_exit_rect, w_surface,
                     found_items_rects, new_map_data):
    if current_map_entrance_rect.collidepoint(
            (int(player.x + (player.width / 2)), int(player.y + (player.height / 2)))):
        current_map_music = current_map.map_music
        map_id -= 1
        player.x = 832
        player.y = current_map_entrance_rect[1]
        surface.blit(map_tuple[map_id].map_background, (0, 0))
        surface.blit(player.load_img(), (player.x, player.y))
        current_map = map_tuple[map_id]
        current_wall_rects = current_map.wall_rects
        drawn_map_entrance = current_map.map_entrance
        drawn_map_exit = current_map.map_exit
        if current_map.map_music != current_map_music:
            soundtrack.load(current_map.map_music)
        # soundtrack.play(-1)
        if drawn_map_entrance is None:
            current_map_entrance_rect = pygame.Rect(-64, -64, 0, 0)
        else:
            current_map_entrance_rect = pygame.Rect(drawn_map_entrance[0], drawn_map_entrance[1], 64, 64)
        if drawn_map_exit is None:
            current_map_exit_rect = pygame.Rect(-64, -64, 0, 0)
        else:
            current_map_exit_rect = pygame.Rect(drawn_map_exit[0], drawn_map_exit[1], 64, 64)
        surface.blit(entrance_img, current_map_entrance_rect)
        surface.blit(exit_img, current_map_exit_rect)
        w_surface.blit(wall1, (0, 0))
        for w_rect in current_wall_rects:
            surface.blit(w_surface, w_rect)
        current_opponents_rects = current_map.opponents_rects
        for o_rect in current_opponents_rects:
            surface.blit(enemy1.load_img(), (o_rect[0], o_rect[1]))
        current_map_items_rects = current_map.map_items_rects
        for i_rect in current_map_items_rects:
            if i_rect not in found_items_rects:
                surface.blit(item_img, i_rect)
        pygame.display.flip()
        new_map_data = (
            map_id, current_map, current_map_entrance_rect, current_map_exit_rect, current_wall_rects,
            current_opponents_rects,
            current_map_items_rects)
        return new_map_data
    elif current_map_exit_rect.collidepoint((int(player.x + (player.width / 2)), int(player.y + (player.height / 2)))):
        current_map_music = current_map.map_music
        map_id += 1
        player.x = 64
        player.y = current_map_exit_rect[1]
        surface.blit(map_tuple[map_id].map_background, (0, 0))
        surface.blit(player.load_img(), (player.x, player.y))
        current_map = map_tuple[map_id]
        current_wall_rects = current_map.wall_rects
        drawn_map_entrance = current_map.map_entrance
        drawn_map_exit = current_map.map_exit
        if current_map.map_music != current_map_music:
            soundtrack.load(current_map.map_music)
        # soundtrack.play(-1)
        if drawn_map_entrance is None:
            current_map_entrance_rect = pygame.Rect(-64, -64, 0, 0)
        else:
            current_map_entrance_rect = pygame.Rect(drawn_map_entrance[0], drawn_map_entrance[1], 64, 64)
        if drawn_map_exit is None:
            current_map_exit_rect = pygame.Rect(-64, -64, 0, 0)
        else:
            current_map_exit_rect = pygame.Rect(drawn_map_exit[0], drawn_map_exit[1], 64, 64)
        surface.blit(entrance_img, current_map_entrance_rect)
        surface.blit(exit_img, current_map_exit_rect)
        w_surface.blit(wall1, (0, 0))
        for w_rect in current_wall_rects:
            surface.blit(w_surface, w_rect)
        current_opponents_rects = current_map.opponents_rects
        for o_rect in current_opponents_rects:
            surface.blit(enemy1.load_img(), (o_rect[0], o_rect[1]))
        current_map_items_rects = current_map.map_items_rects
        for i_rect in current_map_items_rects:
            if i_rect not in found_items_rects:
                surface.blit(item_img, i_rect)
        pygame.display.flip()
        new_map_data = (
            map_id, current_map, current_map_entrance_rect, current_map_exit_rect, current_wall_rects,
            current_opponents_rects,
            current_map_items_rects)
        return new_map_data
    else:
        return new_map_data
