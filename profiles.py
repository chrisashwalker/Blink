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


# Chases the character; the incremental increase or decrease to x,y represents the speed and direction of opponent
def chase(opponent_x, opponent_y, player_x, player_y, walls):
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
        return new_x, new_y
    else:
        return opponent_x, opponent_y
