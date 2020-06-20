from shared import *

pygame.init()


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

class Character:
    def __init__(self, name, base_hp, base_ap, st, bst, rest, speed, x, y):
        self.name = name
        self.base_hp = base_hp
        self.base_ap = base_ap
        self.st = st
        self.bst = bst
        self.rest = rest
        self.speed = speed
        self.x = x
        self.y = y
        self.width = char_width
        self.height = char_height
        self.img = os.path.join('images', (self.name + '.png'))

    def load_img(self):
        return pygame.image.load(self.img).convert_alpha()


# Character declarations
hero = Character('Hero', 10, 5, 2, 4, 1, 10, 0, 0)
enemy1 = Character('Enemy1', 5, 5, 1, 2, 0, 5, -64, -64)
