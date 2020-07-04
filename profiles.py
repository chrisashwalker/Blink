import os
import pygame
import random
import time

from shared import window_width, window_height, char_width, char_height, trans_surface


class Character:
    def __init__(self, name, health, strength, speed):
        # noinspection PyCallByClass,PyTypeChecker
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.health = health
        self.strength = strength
        self.speed = speed

        self.width = char_width
        self.height = char_height
        self.image = os.path.join('graphics', (self.name + '.png'))
        self.surface = pygame.image.load(self.image).convert_alpha()
        self.rect = self.surface.get_rect()


hero = Character('Hero', 10, 2, 5)


# Opponents chase the player when visibility line is not obscured by walls; otherwise, randomly wander around the map

def chase(opponent_x, opponent_y, player_x, player_y, walls, last_direction_x, last_direction_y, last_wander):
    # Only allow a change of direction every five seconds
    wander_change = time.time()
    if wander_change > last_wander + 5:
        direction_x = random.randint(-1, 1)
        direction_y = random.randint(-1, 1)
        last_wander = wander_change
    else:
        direction_x = last_direction_x
        direction_y = last_direction_y

    # Draw a line between the opponent and the player; movement following that line and stopping when a wall intersects
    chase_line = pygame.draw.line(
        trans_surface, (0, 0, 0, 0), (opponent_x + 32, opponent_y + 32), (player_x + 32, player_y + 32), 1)
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

    # Wander around the map, once every 2 seconds, avoiding walls and screen boundaries
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

    # If the opponent can't see the player and it isn't time to wander yet, just return the last results
    else:
        return opponent_x, opponent_y, direction_x, direction_y, last_wander
