import pygame
import random
import time

from shared import window, text, WHITE, BLACK, hit
from images import hit_image
from strings import weapon_upgrade

# Declare option / message positions onscreen
OPT1_POS = (420, 440)
OPT2_POS = (420, 500)
OPT3_POS = (420, 540)
PLAYER_POS = (380, 260)
OPPONENT_POS = (580, 260)
WINNER_POS = (420, 240)
RESULT_MSG_POS = (420, 160)


class Status:
    def __init__(self, hp):
        self.hp = hp


# Battle arena function - process a battle between the hero and an opponent

def arena(player, opponent, player_inventory):
    player_status = Status(player.health)
    opponent_status = Status(opponent.health)
    attack_option = text.render('Attack', True, WHITE)
    use_item_option = text.render('Use an item', True, WHITE)
    attack_rect = attack_option.get_rect(topleft=OPT1_POS)
    use_item_rect = use_item_option.get_rect(topleft=OPT2_POS)
    risky_attack_option = text.render('Attempt a heavy attack', True, WHITE)
    risky_attack_rect = risky_attack_option.get_rect(topleft=OPT3_POS)

    while player_status.hp > 0 and opponent_status.hp > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        mouse_pos = pygame.mouse.get_pos()
        window.fill(BLACK)
        window.blit(player.surface, PLAYER_POS)
        window.blit(opponent.surface, OPPONENT_POS)
        window.blit(attack_option, OPT1_POS)
        window.blit(use_item_option, OPT2_POS)
        window.blit(risky_attack_option, OPT3_POS)
        pygame.draw.rect(window, (255, 0, 0), pygame.Rect(380, 210, player_status.hp * 10, 15))
        pygame.draw.rect(window, (255, 0, 0), pygame.Rect(580, 210, opponent_status.hp * 10, 15))
        pygame.display.flip()

        # Process actions where mouse clicks on rects spanning the rendered text. Player goes first, then opponent
        if attack_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (1, 0, 0):
            risk = False
            action(player, opponent_status, attack_rect, use_item_rect, risky_attack_rect,
                   risk, player, player_inventory)
            hit.play()
            time.sleep(0.5)
            if player_status.hp > 0 and opponent_status.hp > 0:
                action(opponent, player_status, attack_rect, use_item_rect, risky_attack_rect,
                       risk, player, player_inventory)
                hit.play()
                time.sleep(0.5)

        # Item use handling. TODO: Improve item listing and usage
        if use_item_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (1, 0, 0):
            item_list_text = ''
            i = 1
            for each_item in player_inventory.items:
                if each_item.item_type == weapon_upgrade:
                    continue
                else:
                    item_list_text += 'Type 0 to Cancel;     ' + str(i) + ' for ' + each_item.item_name + ';     '
                    i += 1
            item_list = text.render(item_list_text, True, WHITE)
            if i > 1:
                window.fill(BLACK, attack_rect)
                window.fill(BLACK, use_item_rect)
                window.fill(BLACK, risky_attack_rect)
                window.blit(item_list, (430 - len(player_inventory.items) * 50, 500))
                pygame.display.flip()
                while i > 1:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    pressed_keys = pygame.key.get_pressed()

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
                        player_inventory.items[3].use_item(player_status, opponent_status)
                        player_inventory.remove_item(player_inventory.items[3])
                        i = 1
                    if pressed_keys[pygame.K_5]:
                        player_inventory.items[4].use_item(player_status, opponent_status)
                        player_inventory.remove_item(player_inventory.items[4])
                        i = 1
                    if pressed_keys[pygame.K_6]:
                        player_inventory.items[5].use_item(player_status, opponent_status)
                        player_inventory.remove_item(player_inventory.items[5])
                        i = 1
                window.fill(BLACK, use_item_rect)

        if risky_attack_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (1, 0, 0):
            risk = True
            action(player, opponent_status, attack_rect, use_item_rect, risky_attack_rect,
                   risk, player, player_inventory)
            hit.play()
            time.sleep(0.5)
            if player_status.hp > 0 and opponent_status.hp > 0:
                action(opponent, player_status, attack_rect, use_item_rect, risky_attack_rect,
                       risk, player, player_inventory)
                hit.play()
                time.sleep(0.5)

    # The loop - and therefore, battle - ends when either the player or opponent has 0 HP
    if player_status.hp <= 0:
        end_battle(opponent, player_status)
    elif opponent_status.hp <= 0:
        end_battle(player, player_status)
    if player_status.hp > 0:
        return True
    else:
        return False


# Action function - process attacks and display the effects
def action(source, target_stat, attack_rect, use_item_rect, risky_attack_rect, risk, player,
           player_inventory):
    if source == player:
        weapon_power = 0
        if player_inventory.held_weapon is not None:
            weapon_power = player_inventory.held_weapon.item_power
        if risk:
            damage = (source.strength + weapon_power) * random.randint(0, 3)
        else:
            damage = (source.strength + weapon_power)
        window.blit(hit_image, OPPONENT_POS)
    else:
        if risk:
            damage = (source.strength * random.randint(1, 2))
        else:
            damage = source.strength
        window.blit(hit_image, PLAYER_POS)
    target_stat.hp -= damage
    window.fill(BLACK, attack_rect)
    window.fill(BLACK, use_item_rect)
    window.fill(BLACK, risky_attack_rect)
    pygame.display.flip()


# End of battle function - congratulate or commiserate player before returning back to the main game
def end_battle(winner, player_stat):
    if player_stat.hp > 0:
        battle_result = 'You win!'
    else:
        battle_result = 'Game over.'

    window.fill(BLACK)
    msg = text.render(battle_result, True, WHITE)
    window.blit(winner.surface, WINNER_POS)
    window.blit(msg, RESULT_MSG_POS)
    pygame.display.flip()
    loop = True
    time.sleep(0.1)
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RETURN] or pygame.mouse.get_pressed() == (1, 0, 0):
            loop = False
