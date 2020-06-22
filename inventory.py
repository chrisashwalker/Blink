from shared import *


class Item:
    def __init__(self, item_name, item_type, item_power):
        # noinspection PyCallByClass,PyTypeChecker
        pygame.sprite.Sprite.__init__(self)
        self.item_name = item_name
        self.item_type = item_type
        self.item_power = item_power
        self.surface = item_img
        self.rect = self.surface.get_rect()

    def use_item(self, player_status, opponent_status):
        if self.item_type == 'Use once to boost HP during battle':
            player_status.hp += self.item_power
        elif self.item_type == 'Use once to damage the opponent during battle':
            opponent_status.hp -= self.item_power


class Backpack:
    def __init__(self, held_weapon, item_capacity):
        self.held_weapon = held_weapon
        self.item_capacity = item_capacity
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def replace_item(self, item, discarded_item):
        self.items.remove(discarded_item)
        self.items.append(item)

    def remove_item(self, discarded_item):
        self.items.remove(discarded_item)


# Items:
potion = Item('Potion', 'Use once to boost HP during battle', 3)
rock = Item('Rock', 'Use once to damage the opponent during battle', 2)
pin = Item('Rolling Pin', 'Weapon upgrade', 1)
new_backpack = Item('New Backpack', 'Increased storage capacity by 1', 0)
items_list = [potion, rock, pin, new_backpack]
