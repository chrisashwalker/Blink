import pygame
import random

from shared import tile_width, tile_height, track2
from profiles import Character
from images import bg3, wall1


# Convert a string of descriptive characters into a set of map coordinates held in a dictionary
def get_level(level_layout):
    level_coords = {}
    string_char = -1
    for coord_x in range(15):
        for coord_y in range(10):
            string_char += 1
            level_coords[(coord_x * tile_width, coord_y * tile_height)] = level_layout[string_char]
    return level_coords


# Design levels either randomly or based on defined layout arguments
class Level:
    def __init__(self, level_no=1, level_type=1, level_coords=None, wall_freq=5, opponent_freq=75, item_freq=1200):

        # Define level types with set backgrounds, wall graphics and music
        # TODO: Make more and define set level layouts for special areas and boss battles
        # Tuple index order: background, blink background, wall graphic, music track
        level_types = [(1, bg3, bg3, wall1, track2)]

        self.level_no = level_no
        self.level_type = level_type
        self.level_background = level_types[self.level_type - 1][1]
        self.blink_background = level_types[self.level_type - 1][2]
        self.wall_image = level_types[self.level_type - 1][3]
        self.level_music = level_types[self.level_type - 1][4]
        self.level_layout = ''
        opponents_pos = []
        opponent_id = -1

        if level_coords is None:
            self.level_coords = {}

            self.wall_rects = []
            self.opponents = []
            self.level_items_pos = []

            # Draw an empty level of coordinates
            for coord_x in range(15):
                for coord_y in range(10):
                    self.level_coords[(coord_x * tile_width, coord_y * tile_height)] = '.'

            # Draw a clear path from entrance to exit
            entrance_x = 0
            entrance_y = random.randint(0, 9)
            clear_path = {(entrance_x, entrance_y * tile_height),
                          (entrance_x + tile_width, entrance_y * tile_height),
                          (entrance_x + tile_width, entrance_y * tile_height + tile_height),
                          (entrance_x + tile_width, entrance_y * tile_height - tile_height),
                          (entrance_x, entrance_y * tile_height + tile_height),
                          (entrance_x, entrance_y * tile_height - tile_height)}
            next_path_x = entrance_x
            next_path_y = entrance_y
            while next_path_x < 14:
                last_path_x = next_path_x
                next_path_x += random.randint(0, 1)
                if next_path_x == last_path_x:
                    next_path_y = next_path_y + random.choice([-1, 1])
                    if next_path_y < 0:
                        next_path_y += 2
                    elif next_path_y > 9:
                        next_path_y -= 1
                clear_path.add((next_path_x * tile_width, next_path_y * tile_height))
            exit_x = next_path_x
            exit_y = next_path_y
            self.level_entrance = (entrance_x, entrance_y * tile_height)
            self.level_exit = (exit_x * tile_width, exit_y * tile_height)
            self.level_coords[self.level_entrance] = 'A'
            self.level_coords[self.level_exit] = 'B'

            # Randomly generate walls, items and opponents; each with different probabilities
            # Add the results to a level_layout string so that it can be stored in the game save database and redrawn
            for coord in self.level_coords:
                if coord not in clear_path:
                    wall_gamble = random.randint(1, wall_freq)
                    opponent_gamble = random.randint(1, opponent_freq)
                    item_gamble = random.randint(1, item_freq)
                    if wall_gamble == 1:
                        self.wall_rects.append(pygame.Rect(coord, (tile_width, tile_height)))
                        self.level_coords[coord] = 'X'
                    elif opponent_gamble == 1:
                        opponents_pos.append(coord)
                        self.level_coords[coord] = 'O'
                    elif item_gamble == 1:
                        self.level_items_pos.append(coord)
                        self.level_coords[coord] = 'I'
                self.level_layout += self.level_coords[coord]

        # The level layout has been saved, so it should be redrawn upon game load
        else:
            self.level_coords = level_coords
            self.wall_rects = []
            self.opponents = []
            self.level_items_pos = []
            for coord in self.level_coords:
                if self.level_coords[coord] == 'I':
                    self.level_items_pos.append(coord)
                elif self.level_coords[coord] == 'O':
                    opponents_pos.append(coord)
                elif self.level_coords[coord] == 'X':
                    self.wall_rects.append(pygame.Rect(coord, (tile_width, tile_height)))
                elif self.level_coords[coord] == 'A':
                    self.level_entrance = coord
                elif self.level_coords[coord] == 'B':
                    self.level_exit = coord
                self.level_layout += self.level_coords[coord]

        # Create instances of the opponent characters based on drawn opponent positions
        for opponent_pos in opponents_pos:
            opponent_type = random.randint(1, 3)
            opponent_id += 1
            self.opponents.append(Character('Enemy' + str(opponent_type), 10, 3, 4))
            self.opponents[opponent_id].rect.x = opponent_pos[0]
            self.opponents[opponent_id].rect.y = opponent_pos[1]
