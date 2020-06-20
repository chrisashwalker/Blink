import pygame
pygame.init()
from profiles import *

class item:
	def __init__ (self, item_name, item_type, item_power):
		self.item_name = item_name
		self.item_type = item_type
		self.item_power = item_power
		
	def use_item (self, player_status, opponent_status):
		if self.item_type == 'Use once to boost HP during battle':
			player_status.hp += self.item_power
		elif self.item_type == 'Use once to damage the opponent during battle':
			opponent_status.hp -= self.item_power
		#elif self.item_type == 'Weapon upgrade':
			#opponent_status.hp -= self.item_power

class backpack:
	def __init__ (self, held_weapon, item_capacity):
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
potion = item('Potion', 'Use once to boost HP during battle', 3)
rock = item('Rock', 'Use once to damage the opponent during battle', 2)
pin = item('Rolling Pin', 'Weapon upgrade', 1)

items_tuple = (potion, rock, pin)

