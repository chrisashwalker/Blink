import random
import time

from shared import *

# Character object:
# name
# base health points
# strength
# movement speed
# position x coordinate
# position y coordinate


class Character:
    def __init__(self, name, base_hp, st, speed, x, y):
        # noinspection PyCallByClass,PyTypeChecker
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.base_hp = base_hp
        self.st = st
        self.speed = speed
        self.x = x
        self.y = y
        self.width = char_width
        self.height = char_height
        self.img = os.path.join('images', (self.name + '.png'))
        self.surface = pygame.image.load(self.img).convert_alpha()
        self.rect = self.surface.get_rect()


# Character declarations

hero = Character('Hero', 10, 2, 10, 0, 0)


# Chases the character when visibility line is not obscured by walls; otherwise randomly wanders around the map

def chase(opponent_x, opponent_y, player_x, player_y, walls, last_direction_x, last_direction_y, last_wander):
    wander_change = time.time()
    if wander_change > last_wander + 5:
        direction_x = random.randint(-1, 1)
        direction_y = random.randint(-1, 1)
        last_wander = wander_change
    else:
        direction_x = last_direction_x
        direction_y = last_direction_y
    chase_line = pygame.draw.line(
        tp_surface, (0, 0, 0, 0), (opponent_x + 32, opponent_y + 32), (player_x + 32, player_y + 32), 1)
    dist_x = opponent_x - player_x
    dist_y = opponent_y - player_y
    if chase_line.collidelist(walls) == -1:
        if dist_x > 0:
            new_x = opponent_x - 1
        else:
            new_x = opponent_x + 1
        if dist_y > 0:
            new_y = opponent_y - 1
        else:
            new_y = opponent_y + 1
        return new_x, new_y, direction_x, direction_y, last_wander
    # Wander around the map, avoiding walls and screen boundaries
    elif wander_change > last_wander + 2 and pygame.Rect(
            (int(opponent_x + direction_x + 64), int(opponent_y + direction_y + 64)), (64, 64)).collidelist(walls) == \
            -1 and pygame.Rect(
            (int(opponent_x + direction_x), int(opponent_y + direction_y)), (64, 64)).collidelist(walls) == \
            -1 and (opponent_x + direction_x + 64) <= window_width and \
            opponent_y + direction_y + 64 <= window_height and (opponent_x + direction_x) >= 0 and \
            opponent_y + direction_y >= 0:
        opponent_x += direction_x
        opponent_y += direction_y
        return opponent_x, opponent_y, direction_x, direction_y, last_wander
    else:
        return opponent_x, opponent_y, direction_x, direction_y, last_wander
