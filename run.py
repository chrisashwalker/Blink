# Main game program
import pygame
import time
import random

from shared import window, window_width, window_height, framerate, text, BLACK, WHITE, soundtrack, tile_width, \
    tile_height, track1, track2, track3, msg_surface, wall_surface, blink_surface  # ,siren
from images import title_image, accident0_image, accident1_image, accident2_image, accident3_image, bedclosed_image, \
    bedopen_image, entrance_image, exit_image, wall1, item_image
from saves import fetch_all_saves, save_game
from strings import intro1, intro2, intro3, intro4, intro5, intro6, intro7, intro8, intro9, intro10, intro11, intro12, \
    intro13, intro14, intro15, weapon_upgrade
from inventory import Backpack, items_list, new_backpack
from profiles import hero, chase
from battle import arena
from levels import get_level, Level

if __name__ == "__main__":
    program_run = True
    while program_run:
        title_screen = True
        load_screen = False
        load_data = True
        show_intro = False
        save_data = []
        saves_list = []
        username = ''
        soundtrack.load(track1)
        soundtrack.play(-1)
        recovery_count = 0
        hit_count = 10

        # Present the title screen and launch the game by pressing Enter or left-click
        while title_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_run = False
                    show_intro = False
                    load_screen = False
                    title_screen = False
            if not program_run:
                break
            pressed_keys = pygame.key.get_pressed()
            window.fill(BLACK)
            window.blit(title_image, (160, 113))
            pygame.display.flip()
            if pressed_keys[pygame.K_RETURN] or pygame.mouse.get_pressed() == (1, 0, 0):
                soundtrack.stop()
                window.fill(BLACK)
                pygame.display.flip()
                load_screen = True
                title_screen = False
        if not program_run:
            break
        # Present the load screen with a list of saved games if they exist
        while load_screen:
            pressed_keys = pygame.key.get_pressed()
            try:
                saves_list = fetch_all_saves()
            except Exception:
                pass
            if saves_list and load_data:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        program_run = False
                        load_screen = False
                if not program_run:
                    break
                window.blit(msg_surface, (160, 160))
                ask_load = text.render('Load game? Press the number to load or just 0 to start a new game', True, WHITE)
                ask_load.get_rect(topleft=(50, 20))
                msg_surface.blit(ask_load, (50, 20))
                line = 1
                for save in saves_list:
                    print_out = text.render(
                        str(line) + ': ' + save[0] + '     Progress: Level ' + str(save[1]), True, WHITE)
                    print_out.get_rect(topleft=(50, line * 50))
                    msg_surface.blit(print_out, (50, line * 50))
                    line += 1
                pygame.display.flip()

                # Check for key presses which match the save number and send that save for loading; 0 starts a new game
                # TODO: Allow for mouse-clicks and lift limit on number of saves
                if pressed_keys[pygame.K_1]:
                    save_data = list(saves_list[0])
                    window.fill(BLACK)
                    pygame.display.flip()
                    load_screen = False
                if pressed_keys[pygame.K_2]:
                    save_data = list(saves_list[1])
                    window.fill(BLACK)
                    pygame.display.flip()
                    load_screen = False
                if pressed_keys[pygame.K_3]:
                    save_data = list(saves_list[2])
                    window.fill(BLACK)
                    pygame.display.flip()
                    load_screen = False
                if pressed_keys[pygame.K_4]:
                    save_data = list(saves_list[3])
                    window.fill(BLACK)
                    pygame.display.flip()
                    load_screen = False
                if pressed_keys[pygame.K_0]:
                    load_data = False

            # Start a new game with a new user.
            # TODO: Consider allowing for save deletions and
            #  detecting where a new user already exists in the save database
            else:
                show_intro = False         # TODO: Switch back to True to show the intro
                window.blit(msg_surface, (160, 160))
                msg_surface.fill(BLACK)
                ask_name = text.render('Type your name and press Enter', True, WHITE)
                ask_name.get_rect(topleft=(50, 20))
                msg_surface.blit(ask_name, (50, 20))
                unicode_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        program_run = False
                        load_screen = False
                    if event.type == pygame.KEYDOWN and event.unicode in unicode_string:
                        username += event.unicode
                if not program_run:
                    break
                if pressed_keys[pygame.K_BACKSPACE]:
                    username = username[:-1]
                display_name = text.render(str.upper(username), True, WHITE)
                display_name.get_rect(topleft=(50, 100))
                msg_surface.blit(display_name, (50, 100))
                pygame.display.flip()
                if username and pressed_keys[pygame.K_RETURN]:
                    load_screen = False
            
        if not program_run:
            break

        while show_intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    show_intro = False
                    program_run = False
            if not program_run:
                break
            intro_images = (accident0_image, accident1_image, accident2_image, accident3_image)
            for image in intro_images:
                window.blit(image, (160, 0))
                pygame.display.flip()
                time.sleep(2)
            window.fill(BLACK)
            intro_text = text.render(intro1, True, WHITE)
            intro_text_rect = intro_text.get_rect(center=(480, 320))
            window.blit(intro_text, (intro_text_rect[0], intro_text_rect[1]))
            pygame.display.flip()
            time.sleep(2)
            window.fill(BLACK)
            window.blit(bedclosed_image, (160, 0))
            pygame.display.flip()
            time.sleep(4)
            window.blit(bedopen_image, (160, 0))
            pygame.display.flip()
            time.sleep(2)
            intro_text_rect[0] = 64
            window.fill(BLACK)
            intro_strings = (intro2, intro3, intro4, intro5, intro6, intro7, intro8, intro9, intro10, intro11, intro12,
                             intro13, intro14, intro15)
            for string in intro_strings:
                intro_text = text.render(string, True, WHITE)
                window.blit(intro_text, (intro_text_rect[0], intro_text_rect[1]))
                pygame.display.flip()
                time.sleep(5)
                window.fill(BLACK)
            show_intro = False
        if not program_run:
            break

        # Launch game, set initial variables and load save data, if applicable.
        run_game = True
        soundtrack.load(track2)
        soundtrack.play(-1)
        player_inventory = Backpack(None, 3)
        found_items_rects = []
        msg_surface_rect = msg_surface.get_rect(topleft=(80, 170))
        defeated = []
        wall_collision_index = -1
        last_move = 0
        move = ''
        test_hero_x = 0
        test_hero_y = 0
        last_direction_x = 0
        last_direction_y = 0
        last_wander = 0
        blink = False
        # blink_timer = 1
        # blink_length = 0
        # blink_wait_timer = 0
        # blink_wait_length = random.randint(1800, 3600)

        if save_data:
            if save_data[2]:
                saved_weapon = save_data[2]
                for item in items_list:
                    if item.item_name == saved_weapon:
                        player_inventory = Backpack(item, save_data[3])
            else:
                player_inventory = Backpack(None, save_data[3])

            saved_items = save_data[4].split(',')
            for item in items_list:
                for saved_item in saved_items:
                    if saved_item == item.item_name:
                        player_inventory.items.append(item)

            level_no = save_data[1]
            level_type = save_data[6]
            level_layout = save_data[7]
            level_coords = get_level(level_layout)
            current_level = Level(level_no, level_type, level_coords)
            hero.rect.x = current_level.level_entrance[0] + tile_width
            hero.rect.y = current_level.level_entrance[1]

            # Build a list of items already found on the level so that reloading doesn't respawn all items
            saved_found_items = save_data[5].split('.')
            if saved_found_items[0]:
                for found_item in saved_found_items:
                    found_item_split = found_item.split(',')
                    if not found_items_rects:
                        found_items_rects = [
                            pygame.Rect(int(found_item_split[0]), int(found_item_split[1]), tile_width, tile_height)]
                    else:
                        found_items_rects.append(
                            pygame.Rect(int(found_item_split[0]), int(found_item_split[1]), tile_width, tile_height))

        else:
            level_no = 1
            current_level = Level()
            level_layout = current_level.level_layout
            hero.rect.x = current_level.level_entrance[0] + tile_width
            hero.rect.y = current_level.level_entrance[1]
            save_data = [
                str.upper(username), level_no, '', player_inventory.item_capacity, '', '', current_level.level_type,
                current_level.level_layout]

        # Function to update the screen, with moving characters
        # TODO: Make display updates more efficient
        def display_update(direction_x, direction_y, wander, blink_check):
            msg_surface.fill(BLACK)
            window.blit(current_level.level_background, (0, 0))
            if current_level.level_no > 1:
                window.blit(entrance_image, pygame.Rect(current_level.level_entrance, (tile_width, tile_height)))
            window.blit(exit_image, pygame.Rect(current_level.level_exit, (tile_width, tile_height)))
            wall_surface.blit(wall1, (0, 0))
            chase_results = ()
            for wall_rect in current_level.wall_rects:
                window.blit(wall_surface, wall_rect)
            for level_item in current_level.level_items_pos:
                item_rect = pygame.Rect(level_item, (tile_width, tile_height))
                if item_rect not in found_items_rects:
                    window.blit(item_image, item_rect)
            window.blit(hero.surface, hero.rect)
            if blink_check:
                for level_opponent in current_level.opponents:
                    chase_results = chase(level_opponent.rect[0], level_opponent.rect[1], hero.rect.x, hero.rect.y,
                                          current_level.wall_rects, direction_x, direction_y, wander)
                    if level_opponent not in defeated:
                        level_opponent.rect.x = chase_results[0]
                        level_opponent.rect.y = chase_results[1]
                        window.blit(level_opponent.surface, level_opponent.rect)
                blink_surface.set_alpha(100)
            else:
                blink_surface.set_alpha(0)
            window.blit(blink_surface, (0, 0))
            pygame.display.flip()
            if len(chase_results) > 0:
                return chase_results[2], chase_results[3], chase_results[4]
            else:
                return 0, 0, 0

        def display_update_no_chase(blink_check):
            msg_surface.fill(BLACK)
            window.blit(current_level.level_background, (0, 0))
            if current_level.level_no > 1:
                window.blit(entrance_image, pygame.Rect(current_level.level_entrance, (tile_width, tile_height)))
            window.blit(exit_image, pygame.Rect(current_level.level_exit, (tile_width, tile_height)))
            wall_surface.blit(wall1, (0, 0))
            for wall_rect in current_level.wall_rects:
                window.blit(wall_surface, wall_rect)
            for level_item in current_level.level_items_pos:
                item_rect = pygame.Rect(level_item, (tile_width, tile_height))
                if item_rect not in found_items_rects:
                    window.blit(item_image, item_rect)
            window.blit(hero.surface, hero.rect)
            if blink_check:
                for level_opponent in current_level.opponents:
                    if level_opponent not in defeated:
                        window.blit(level_opponent.surface, level_opponent.rect)
                blink_surface.set_alpha(100)
            else:
                blink_surface.set_alpha(0)
            window.blit(blink_surface, (0, 0))
            pygame.display.flip()

        # Main game loop
        while run_game:

            framerate.tick(60)
            hero.speed = 4

            # Listen for the window being closed and quit the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False

            # Check what key is pressed in the current iteration of the game loop
            pressed_keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            # Redraw the map, characters and objects in each loop, to pick up changes
            last_direction_x = display_update(last_direction_x, last_direction_y, last_wander, blink)[0]
            last_direction_y = display_update(last_direction_x, last_direction_y, last_wander, blink)[1]
            last_wander = display_update(last_direction_x, last_direction_y, last_wander, blink)[2]

            # Run 'blinks' randomly, which activate/deactivate opponent characters
            # TODO: Deactivate level change blink choice, activate this, blink variables and
            #  shared.siren if still wanted
            # if blink_timer <= blink_length and blink_wait_timer > blink_wait_length:
            #     blink = True
            #     blink_timer += 1
            # elif blink_timer > blink_length and blink_wait_timer > blink_wait_length:
            #     blink = True
            #     blink_wait_timer = 0
            #     blink_wait_length = random.randint(1800, 3600)
            #     window.fill((255, 255, 255))
            #     pygame.display.flip()
            #     time.sleep(0.5)
            #     soundtrack.play(-1)
            # elif blink_timer > blink_length and blink_wait_timer == blink_wait_length:
            #     blink = False
            #     blink_timer = 0
            #     blink_length = random.randint(3600, 7200)
            #     blink_wait_timer += 1
            #     window.fill((255, 255, 255))
            #     pygame.display.flip()
            #     time.sleep(0.5)
            # elif blink_timer > blink_length and blink_wait_timer < blink_wait_length:
            #     if blink_wait_timer + 750 == blink_wait_length:
            #         soundtrack.stop()
            #         siren.play(2)
            #     blink = False
            #     blink_wait_timer += 1

            # Check for keyboard input and test the proposed movement fits the boundaries of the window and wall layout
            # TODO: New - needs tidying
            if time.time() - last_move > 0.1 and (pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_RIGHT] or
                                                  pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_DOWN]):
                if pressed_keys[pygame.K_LEFT]:
                    move = 'left'
                    test_hero_x = hero.rect.x - hero.width
                    test_hero_y = hero.rect.y
                if pressed_keys[pygame.K_RIGHT]:
                    move = 'right'
                    test_hero_x = hero.rect.x + hero.width
                    test_hero_y = hero.rect.y
                if pressed_keys[pygame.K_UP]:
                    move = 'up'
                    test_hero_x = hero.rect.x
                    test_hero_y = hero.rect.y - hero.height
                if pressed_keys[pygame.K_DOWN]:
                    move = 'down'
                    test_hero_x = hero.rect.x
                    test_hero_y = hero.rect.y + hero.height
                wall_collision_index = pygame.Rect(
                    test_hero_x, test_hero_y, hero.width, hero.height).collidelist(current_level.wall_rects)
                if wall_collision_index == -1:
                    if move == 'left' and hero.rect.x - hero.width >= 0:
                        while (hero.rect.x - hero.speed) % hero.width != 0:
                            hero.rect.x -= hero.speed
                            display_update_no_chase(blink)
                        hero.rect.x -= hero.speed
                    elif move == 'right' and hero.rect.x + hero.width * 2 <= window_width:
                        while (hero.rect.x + hero.speed) % hero.width != 0:
                            hero.rect.x += hero.speed
                            display_update_no_chase(blink)
                        hero.rect.x += hero.speed
                    elif move == 'up' and hero.rect.y - hero.height >= 0:
                        while (hero.rect.y - hero.speed) % hero.height != 0:
                            hero.rect.y -= hero.speed
                            display_update_no_chase(blink)
                        hero.rect.y -= hero.speed
                    elif move == 'down' and hero.rect.y + hero.height * 2 <= window_height:
                        while (hero.rect.y + hero.speed) % hero.height != 0:
                            hero.rect.y += hero.speed
                            display_update_no_chase(blink)
                        hero.rect.y += hero.speed
                move = ''
                last_move = time.time()

                # Check for level changes and save the game automatically
                # TODO: New - needs tidying; build in entrance travel and store past level layouts
                if pygame.Rect(current_level.level_exit, (tile_width, tile_height)).colliderect(hero.rect):
                    level_no += 1
                    current_level = Level(level_no)
                    level_type = current_level.level_type
                    hero.rect.x = tile_width
                    hero.rect.y = current_level.level_entrance[1]
                    level_layout = current_level.level_layout
                    save_data[1] = level_no
                    save_data[6] = level_type
                    save_data[7] = level_layout
                    blink = random.choice([True, False])

                    if player_inventory.held_weapon:
                        save_data[2] = player_inventory.held_weapon.item_name
                    save_data[3] = player_inventory.item_capacity
                    inventory_items = ''
                    for inventory_item in player_inventory.items:
                        if inventory_items == '':
                            inventory_items = inventory_item.item_name
                        else:
                            inventory_items += ',' + inventory_item.item_name
                    save_data[4] = inventory_items

                    found_items = ''
                    for found_item in found_items_rects:
                        if found_items == '':
                            found_items = str(found_item[0]) + ',' + str(found_item[1])
                        else:
                            found_items += '.' + str(found_item[0]) + ',' + str(found_item[1])
                    save_data[5] = found_items

                    save_game(
                        save_data[0], save_data[1], save_data[2], save_data[3],
                        save_data[4], save_data[5], save_data[6], save_data[7])

            # Check for collisions between player and opponents to start a battle or a fight
            if blink:
                for opponent in current_level.opponents:
                    if hero.rect.colliderect(opponent.rect) and opponent not in defeated:
                        if opponent.name not in ['Enemy1', 'Enemy2', 'Enemy3']:
                            time.sleep(1)
                            defeated.append(opponent)
                            soundtrack.stop()
                            soundtrack.load(track3)
                            soundtrack.set_volume(0.4)
                            soundtrack.play(-1)
                            run_game = arena(hero, opponent, player_inventory)
                            soundtrack.stop()
                            soundtrack.set_volume(0.9)
                            soundtrack.load(current_level.level_music)
                            soundtrack.play(-1)
                        else:
                            if time.time() > recovery_count + 7:
                                recovery_count = time.time()
                                hit_count = hero.health
                            hit_count -= opponent.strength / 50
                            if pressed_keys[pygame.K_SPACE]:
                                opponent.health -= hero.strength
                                hit_count += opponent.strength
                                if hit_count > hero.health:
                                    hit_count = hero.health

            for lvl_opponent in current_level.opponents:
                if lvl_opponent.health < 1:
                    defeated.append(lvl_opponent)

            if hit_count < 1:
                run_game = False

            # Item pickup and storage handling
            # TODO: New - needs tidying
            i0 = min(0, len(player_inventory.items) - 1)
            i1 = min(1, len(player_inventory.items) - 1)
            i2 = min(2, len(player_inventory.items) - 1)
            i3 = min(3, len(player_inventory.items) - 1)
            i4 = min(4, len(player_inventory.items) - 1)
            i5 = min(5, len(player_inventory.items) - 1)
            backpack_add_once = True

            for item_test in current_level.level_items_pos:
                item_test_rect = pygame.Rect(item_test, (tile_width, tile_height))
                if hero.rect.colliderect(item_test_rect) and item_test_rect not in found_items_rects:
                    item_wait = True
                    if player_inventory.item_capacity >= 6 and new_backpack in items_list:
                        items_list.remove(new_backpack)
                    random_item_index = random.randint(0, len(items_list) - 1)
                    random_item = items_list[random_item_index]
                    while item_wait:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run_game = False
                                item_wait = False
                        mouse_pos = pygame.mouse.get_pos()

                        if random_item.item_name == 'New Backpack':
                            if backpack_add_once:
                                player_inventory.item_capacity += 1
                                backpack_add_once = False
                            found_item_text = text.render(
                                'You found a ' + random_item.item_name + '. ' + random_item.item_type, True, WHITE)

                        elif random_item.item_type == weapon_upgrade:
                            if player_inventory.held_weapon is not None:
                                weapon_power = player_inventory.held_weapon.item_power
                            else:
                                weapon_power = 0
                            found_item_text = text.render('You found a ' + random_item.item_name + ' (power lvl: ' +
                                                          str(random_item.item_power) +
                                                          '). Use it as your main weapon? Current weapon power lvl: ' +
                                                          str(weapon_power), True, WHITE)
                            add_option = text.render('Use it', True, WHITE)
                            add_option_rect = add_option.get_rect(topleft=(50, 80))
                            msg_surface.blit(add_option, (50, 80))
                            discard_option = text.render('Discard it', True, WHITE)
                            discard_option_rect = discard_option.get_rect(topleft=(50, 120))
                            msg_surface.blit(discard_option, (50, 120))
                            if add_option_rect.collidepoint(mouse_pos[0] - 80, mouse_pos[1] - 170) and \
                                    pygame.mouse.get_pressed() == (1, 0, 0):
                                player_inventory.held_weapon = random_item

                        elif random_item.item_name != 'New Backpack' and random_item.item_type != weapon_upgrade and \
                                len(player_inventory.items) < player_inventory.item_capacity:
                            found_item_text = text.render('You found a ' + random_item.item_name + ' (power lvl: ' +
                                                          str(random_item.item_power) +
                                                          '). Add it to your inventory?', True, WHITE)
                            add_option = text.render('Add it', True, WHITE)
                            add_option_rect = add_option.get_rect(topleft=(50, 80))
                            msg_surface.blit(add_option, (50, 80))
                            discard_option = text.render('Discard it', True, WHITE)
                            discard_option_rect = discard_option.get_rect(topleft=(50, 120))
                            msg_surface.blit(discard_option, (50, 120))
                            if add_option_rect.collidepoint(mouse_pos[0] - 80, mouse_pos[1] - 170) and \
                                    pygame.mouse.get_pressed() == (1, 0, 0):
                                player_inventory.add_item(random_item)

                        else:
                            found_item_text = text.render('You found a ' + random_item.item_name + ' (Power: ' + str(
                                random_item.item_power) + '), but your inventory is full. Replace it with something?',
                                                          True, WHITE)
                            discard_option = text.render('Discard it', True, WHITE)
                            discard_option_rect = discard_option.get_rect(topleft=(50, 80))
                            msg_surface.blit(discard_option, (50, 80))
                            replace_option1 = text.render('Replace it with ' + player_inventory.items[i0].item_name,
                                                          True, WHITE)
                            replace_option1_rect = replace_option1.get_rect(topleft=(50, 120))
                            if len(player_inventory.items) >= 1:
                                msg_surface.blit(replace_option1, (50, 120))
                            replace_option2 = text.render('Replace it with ' + player_inventory.items[i1].item_name,
                                                          True, WHITE)
                            replace_option2_rect = replace_option2.get_rect(topleft=(50, 160))
                            if len(player_inventory.items) >= 2:
                                msg_surface.blit(replace_option2, (50, 160))
                            replace_option3 = text.render('Replace it with ' + player_inventory.items[i2].item_name,
                                                          True, WHITE)
                            replace_option3_rect = replace_option3.get_rect(topleft=(50, 200))
                            if len(player_inventory.items) >= 3:
                                msg_surface.blit(replace_option3, (50, 200))
                            replace_option4 = text.render('Replace it with ' + player_inventory.items[i3].item_name,
                                                          True, WHITE)
                            replace_option4_rect = replace_option4.get_rect(topleft=(50, 240))
                            if len(player_inventory.items) >= 4:
                                msg_surface.blit(replace_option4, (50, 240))
                            replace_option5 = text.render('Replace it with ' + player_inventory.items[i4].item_name,
                                                          True, WHITE)
                            replace_option5_rect = replace_option5.get_rect(topleft=(50, 280))
                            if len(player_inventory.items) >= 5:
                                msg_surface.blit(replace_option5, (50, 280))
                            replace_option6 = text.render('Replace it with ' + player_inventory.items[i5].item_name,
                                                          True, WHITE)
                            replace_option6_rect = replace_option6.get_rect(topleft=(50, 320))
                            if len(player_inventory.items) >= 6:
                                msg_surface.blit(replace_option6, (50, 320))
                            if replace_option1_rect.collidepoint(mouse_pos[0] - 80, mouse_pos[1] - 170) and \
                                    pygame.mouse.get_pressed() == (1, 0, 0):
                                player_inventory.replace_item(random_item, player_inventory.items[i0])
                            elif replace_option2_rect.collidepoint(mouse_pos[0] - 80, mouse_pos[1] - 170) and \
                                    pygame.mouse.get_pressed() == (1, 0, 0):
                                player_inventory.replace_item(random_item, player_inventory.items[i1])
                            elif replace_option3_rect.collidepoint(mouse_pos[0] - 80, mouse_pos[1] - 170) and \
                                    pygame.mouse.get_pressed() == (1, 0, 0):
                                player_inventory.replace_item(random_item, player_inventory.items[i2])
                            elif replace_option4_rect.collidepoint(mouse_pos[0] - 80, mouse_pos[1] - 170) and \
                                    pygame.mouse.get_pressed() == (1, 0, 0):
                                player_inventory.replace_item(random_item, player_inventory.items[i3])
                            elif replace_option5_rect.collidepoint(mouse_pos[0] - 80, mouse_pos[1] - 170) and \
                                    pygame.mouse.get_pressed() == (1, 0, 0):
                                player_inventory.replace_item(random_item, player_inventory.items[i4])
                            elif replace_option6_rect.collidepoint(mouse_pos[0] - 80, mouse_pos[1] - 170) and \
                                    pygame.mouse.get_pressed() == (1, 0, 0):
                                player_inventory.replace_item(random_item, player_inventory.items[i5])

                        found_item_text_rect = found_item_text.get_rect(topleft=(50, 40))
                        msg_surface.blit(found_item_text, (50, 40))
                        msg_surface_rect = msg_surface.get_rect(topleft=(80, 170))
                        window.blit(msg_surface, (80, 170))
                        pygame.display.update(msg_surface_rect)
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            found_items_rects.append(item_test_rect)
                            item_wait = False

    pygame.quit()
