import pygame
pygame.init()
import time
import random
from shared import *
from profiles import *
from inventory import *

OPT1_POS = (420, 440)
OPT2_POS = (420, 500)
OPT3_POS = (420, 540)
PLAYER_POS = (380, 260)
OPPONENT_POS = (580, 260)
HUD_POS = (420, 160)
ACTION_MSG_POS = (420, 440)
WINNER_POS = (420, 240)
RESULT_MSG_POS = (420, 160)

# Status object
	# health points
	# ability points
	# restoration status
	
class status:
	def __init__(stat, hp, ap, rest_status):
		stat.hp = hp
		stat.ap = ap
		stat.rest_status = rest_status

#Battle arena function - process a battle between the hero and an opponent
	
def arena(player, opponent, player_inventory):
	player_status = status(player.base_hp, player.base_ap, player.rest)
	opponent_status = status(opponent.base_hp, opponent.base_ap, opponent.rest)
	attack_option = text.render('Attack', True, WHITE)
	use_item_option = text.render('Use an item', True, WHITE)
	attack_rect = attack_option.get_rect(topleft = OPT1_POS)
	use_item_rect = use_item_option.get_rect(topleft = OPT2_POS)
	risky_attack_option = text.render('Attempt a heavy attack', True, WHITE)
	risky_attack_rect = risky_attack_option.get_rect(topleft = OPT3_POS)
	
	while player_status.hp > 0 and opponent_status.hp > 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		pressed_keys = pygame.key.get_pressed()
		mouse_pos = pygame.mouse.get_pos()
		window.fill(BLACK)
		window.blit(player.load_img(), PLAYER_POS)
		window.blit(opponent.load_img(), OPPONENT_POS)
		hud_text = player.name + ': ' + str(player_status.hp) + '     ' + opponent.name + ': ' + str(opponent_status.hp)
		hud = text.render(hud_text, True, WHITE)
		#window.blit(hud, HUD_POS)
		window.blit(attack_option, OPT1_POS)
		window.blit(use_item_option, OPT2_POS)
		window.blit(risky_attack_option, OPT3_POS)
		player_hp_bar = pygame.draw.rect(window, (255, 0, 0), pygame.Rect(380, 210, player_status.hp * 10, 15)) # Tidy up HUD later
		opponent_hp_bar = pygame.draw.rect(window, (255, 0, 0), pygame.Rect(580, 210, opponent_status.hp * 10, 15))
		pygame.display.flip()
		
		# Process battle actions where the mouse clicks on the rects spanning the rendered text options. Currently, the player always goes first, then the opponent takes their turn
		if attack_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (1, 0, 0):
			risk = False
			action(player, opponent, opponent_status, hud_text, hud, attack_rect, use_item_rect, risky_attack_rect, risk, player, player_inventory)

			if player_status.hp > 0 and opponent_status.hp > 0:
				action(opponent, player, player_status, hud_text, hud, attack_rect, use_item_rect, risky_attack_rect, risk, player, player_inventory)

		if use_item_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (1, 0, 0):
			item_list_text = ''
			i = 1
			for each_item in player_inventory.items:
				if each_item.item_type == 'Weapon upgrade':
					continue
				else:
					item_list_text += 'Type 0 to Cancel;     ' + str(i) + ' for ' + each_item.item_name + ';     '
					i += 1
			item_list = text.render(item_list_text, True, WHITE)
			if i > 1:
				window.fill(BLACK, attack_rect)
				window.fill(BLACK, use_item_rect)
				window.fill(BLACK, risky_attack_rect)
				item_list_rect = item_list.get_rect(topleft = OPT2_POS)
				window.blit(item_list, OPT2_POS)
				pygame.display.flip()
				while i > 1:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							run_game = False
			
					pressed_keys = pygame.key.get_pressed()
					
					# Add more with inventory upgrades
					if pressed_keys[pygame.K_0]:
						i = 1
					if pressed_keys[pygame.K_1]:
						player_inventory.items[0].use_item(player_status, opponent_status)
						player_inventory.remove_item(player_inventory.items[0])
						i = 1
					if pressed_keys[pygame.K_2]:
						player_inventory.items[1].use_item(player_status, opponent_status)
						player_inventory.remove_item(player_inventory.items[1])
						i = 1
					if pressed_keys[pygame.K_3]:
						player_inventory.items[2].use_item(player_status, opponent_status)
						player_inventory.remove_item(player_inventory.items[2])
						i = 1
					if pressed_keys[pygame.K_4]:
						i = 1
					if pressed_keys[pygame.K_5]:
						i = 1
					if pressed_keys[pygame.K_6]:
						i = 1
					if pressed_keys[pygame.K_7]:
						i = 1
				window.fill(BLACK, use_item_rect)
		
		if risky_attack_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (1, 0, 0):
			risk = True
			action(player, opponent, opponent_status, hud_text, hud, attack_rect, use_item_rect, risky_attack_rect, risk, player, player_inventory)

			if player_status.hp > 0 and opponent_status.hp > 0:
				action(opponent, player, player_status, hud_text, hud, attack_rect, use_item_rect, risky_attack_rect, risk, player, player_inventory)
	
	# The loop - and therefore, battle - ends when either the player or opponent has 0 HP
	if player_status.hp <= 0:
		end_battle(opponent)
	else:
		end_battle(player)

# Action function - process attacks and display the effects; functionality to be expanded with battle options
	
def action(source, target, target_stat, hud_text, hud, attack_rect, use_item_rect, risky_attack_rect, risk, player, player_inventory):
	if source == player:
		weapon_count = 0
		weapon_power = 0
		for each_item in player_inventory.items:
				if each_item.item_type == 'Weapon upgrade':
					weapon_count += 1
					weapon_power = each_item.item_power
		if risk == True:
			damage = (source.st + weapon_power) * random.randint(0, 3)
		else:
			damage = (source.st + weapon_power)
	else:
		if risk == True:
			damage = (source.st * random.randint(1, 2))
		else:
			damage = source.st
	target_stat.hp -= damage
	action_msg = target.name + ' loses ' + str(damage) + ' health'
	window.fill(BLACK, attack_rect)
	window.fill(BLACK, use_item_rect)
	window.fill(BLACK, risky_attack_rect)
	#window.blit(hud, HUD_POS)
	msg = text.render(action_msg, True, WHITE)
	#window.blit(msg, ACTION_MSG_POS)
	pygame.display.flip()
	#time.sleep(1.5)
	time.sleep(0.1)
	window.fill(BLACK, msg.get_rect(topleft = ACTION_MSG_POS))

# End of battle function - congratulate or commiserate player before returning back to the main game

def end_battle(winner):
	battle_result = 'You win!'
	window.fill(BLACK)
	msg = text.render(battle_result, True, WHITE)
	window.blit(winner.load_img(), WINNER_POS)
	window.blit(msg, RESULT_MSG_POS)
	pygame.display.flip()
	loop = True
	while loop == True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_RETURN] or pygame.mouse.get_pressed() == (1, 0, 0):
			loop = False
