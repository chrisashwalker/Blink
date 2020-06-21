# Main game program

import random

from battle import arena
from inventory import *
from maps import *
from profiles import hero, enemy1

pygame.init()

if __name__ == "__main__":

    title_screen = True
    soundtrack.load(track1)
    soundtrack.play(-1)
    while title_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pressed_keys = pygame.key.get_pressed()
        framerate.tick(60)
        title_text = bigtext.render('Blink - Press Enter to play', True, WHITE)
        title_text_rect = title_text.get_rect()
        window.blit(title_text, (150, 280))
        pygame.display.flip()
        if pressed_keys[pygame.K_RETURN]:
            soundtrack.stop()
            window.fill(BLACK)
            pygame.display.flip()
            title_screen = False

    run_game = True

    window.blit(map_tuple[map_ID].map_background, (0, 0))
    drawn_map = map_tuple[map_ID]
    drawn_opponents_rects = drawn_map.opponents_rects
    pygame.display.flip()
    soundtrack.load(map_tuple[map_ID].map_music)
    defeated_rects = []
    found_items_rects = []
    onscreen_chars = set()
    player_inventory = Backpack(None, 3)

    while run_game:

        # Listen for the window being closed and quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        pressed_keys = pygame.key.get_pressed()  # Check what key is pressed in the current iteration of the game loop
        mouse_pos = pygame.mouse.get_pos()

        framerate.tick(60)

        # Load map and  layout; create off-screen entrance/exit rects if map is missing either, to avoid Type errors
        window.blit(map_tuple[map_ID].map_background, (0, 0))
        drawn_wall_rects = drawn_map.wall_rects
        drawn_map_entrance = drawn_map.map_entrance
        drawn_map_exit = drawn_map.map_exit
        if drawn_map_entrance is None:
            drawn_map_entrance_rect = pygame.Rect(-64, -64, 0, 0)
        else:
            drawn_map_entrance_rect = pygame.Rect(drawn_map_entrance[0], drawn_map_entrance[1], 64, 64)
        if drawn_map_exit is None:
            drawn_map_exit_rect = pygame.Rect(-64, -64, 0, 0)
        else:
            drawn_map_exit_rect = pygame.Rect(drawn_map_exit[0], drawn_map_exit[1], 64, 64)
        wall_surface.blit(wall1, (0, 0))
        for w_rect in drawn_wall_rects:
            window.blit(wall_surface, w_rect)
        window.blit(entrance_img, drawn_map_entrance_rect)
        window.blit(exit_img, drawn_map_exit_rect)
        drawn_map_items_rects = drawn_map.map_items_rects
        new_map_data = (
            map_ID, drawn_map, drawn_map_entrance_rect, drawn_map_exit_rect, drawn_wall_rects, drawn_opponents_rects,
            drawn_map_items_rects)
        for o_rect in drawn_opponents_rects:
            if o_rect not in defeated_rects:
                window.blit(enemy1.load_img(), (o_rect[0], o_rect[1]))

        test_hero_x = -64
        test_hero_y = -64
        wall_collision_index = -1
        hero.speed = 10

        onscreen_chars_rects = [pygame.Rect(hero.x, hero.y, hero.width, hero.height)]
        onscreen_chars_rects.extend(drawn_opponents_rects)

        # Check for keyboard input and test the proposed movement fits the boundaries of the window and map wall layout
        if pressed_keys[pygame.K_LEFT]:
            while hero.speed > 0:
                test_hero_x = hero.x - hero.speed
                test_hero_y = hero.y
                wall_collision_index = pygame.Rect(test_hero_x, test_hero_y, hero.width, hero.height).collidelist(
                    drawn_wall_rects)
                if hero.x - hero.speed >= 0 and wall_collision_index == -1:
                    hero.x -= hero.speed
                    new_map_data = map_change_check(window, hero, map_ID, drawn_map, drawn_map_entrance_rect,
                                                    drawn_map_exit_rect, wall_surface, found_items_rects, new_map_data)
                    map_ID = new_map_data[0]
                    drawn_map = new_map_data[1]
                    drawn_map_entrance_rect = new_map_data[2]
                    drawn_map_exit_rect = new_map_data[3]
                    drawn_wall_rects = new_map_data[4]
                    drawn_opponents_rects = new_map_data[5]
                    drawn_map_items_rects = new_map_data[6]
                    break
                else:
                    hero.speed -= 1

        if pressed_keys[pygame.K_RIGHT]:
            while hero.speed > 0:
                test_hero_x = hero.x + hero.speed
                test_hero_y = hero.y
                wall_collision_index = pygame.Rect(test_hero_x, test_hero_y, hero.width, hero.height).collidelist(
                    drawn_wall_rects)
                if hero.x + hero.width + hero.speed <= window_width and wall_collision_index == -1:
                    hero.x += hero.speed
                    new_map_data = map_change_check(window, hero, map_ID, drawn_map, drawn_map_entrance_rect,
                                                    drawn_map_exit_rect, wall_surface, found_items_rects, new_map_data)
                    map_ID = new_map_data[0]
                    drawn_map = new_map_data[1]
                    drawn_map_entrance_rect = new_map_data[2]
                    drawn_map_exit_rect = new_map_data[3]
                    drawn_wall_rects = new_map_data[4]
                    drawn_opponents_rects = new_map_data[5]
                    drawn_map_items_rects = new_map_data[6]
                    break
                else:
                    hero.speed -= 1

        if pressed_keys[pygame.K_UP]:
            while hero.speed > 0:
                test_hero_x = hero.x
                test_hero_y = hero.y - hero.speed
                wall_collision_index = pygame.Rect(test_hero_x, test_hero_y, hero.width, hero.height).collidelist(
                    drawn_wall_rects)
                if hero.y - hero.speed >= 0 and wall_collision_index == -1:
                    hero.y -= hero.speed
                    new_map_data = map_change_check(window, hero, map_ID, drawn_map, drawn_map_entrance_rect,
                                                    drawn_map_exit_rect, wall_surface, found_items_rects, new_map_data)
                    map_ID = new_map_data[0]
                    drawn_map = new_map_data[1]
                    drawn_map_entrance_rect = new_map_data[2]
                    drawn_map_exit_rect = new_map_data[3]
                    drawn_wall_rects = new_map_data[4]
                    drawn_opponents_rects = new_map_data[5]
                    drawn_map_items_rects = new_map_data[6]
                    break
                else:
                    hero.speed -= 1

        if pressed_keys[pygame.K_DOWN]:
            while hero.speed > 0:
                test_hero_x = hero.x
                test_hero_y = hero.y + hero.speed
                wall_collision_index = pygame.Rect(test_hero_x, test_hero_y, hero.width, hero.height).collidelist(
                    drawn_wall_rects)
                if hero.y + hero.height + hero.speed <= window_height and wall_collision_index == -1:
                    hero.y += hero.speed
                    new_map_data = map_change_check(window, hero, map_ID, drawn_map, drawn_map_entrance_rect,
                                                    drawn_map_exit_rect, wall_surface, found_items_rects, new_map_data)
                    map_ID = new_map_data[0]
                    drawn_map = new_map_data[1]
                    drawn_map_entrance_rect = new_map_data[2]
                    drawn_map_exit_rect = new_map_data[3]
                    drawn_wall_rects = new_map_data[4]
                    drawn_opponents_rects = new_map_data[5]
                    drawn_map_items_rects = new_map_data[6]
                    break
                else:
                    hero.speed -= 1

        # Update rects based on character positions, check for collisions and update parts of screen with changes
        onscreen_chars_rects.append(pygame.Rect(hero.x, hero.y, hero.width, hero.height))

        if pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(drawn_opponents_rects) != -1 and \
                pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(defeated_rects) == -1:
            battle_op_rect_index = \
                pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(drawn_opponents_rects)
            defeated_rects.append(pygame.Rect(drawn_opponents_rects[battle_op_rect_index]))
            arena(hero, enemy1, player_inventory)
            window.blit(map_tuple[map_ID].map_background, (0, 0))
            for w_rect in drawn_wall_rects:
                window.blit(wall_surface, w_rect)
            for i_rect in drawn_map_items_rects:
                if i_rect not in found_items_rects:
                    window.blit(item_img, i_rect)
            window.blit(entrance_img, drawn_map_entrance_rect)
            window.blit(exit_img, drawn_map_exit_rect)
            pygame.display.flip()

        # Item pickup handling; tidy up and minimise this code
        if pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(drawn_map_items_rects) != -1 and \
                pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(found_items_rects) == -1:
            wait = True
            random_item_index = random.randint(0, len(items_tuple) - 1)
            random_item = items_tuple[random_item_index]
            weapon_count = 0
            weapon_power = 0
            for each_item in player_inventory.items:
                if each_item.item_type == 'Weapon upgrade':
                    weapon_power = each_item.item_power
                    weapon_count += 1
            if weapon_count > 0:
                replace_weapon = True
            else:
                replace_weapon = False
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_game = False
                        wait = False
                mouse_pos = pygame.mouse.get_pos()
                if len(player_inventory.items) < player_inventory.item_capacity and \
                        random_item.item_type != 'Weapon upgrade':
                    found_item = text.render('You found a ' + random_item.item_name + ' (power lvl: ' + str(
                        random_item.item_power) + '). Add it to your inventory?', True, WHITE)
                    found_item_rect = found_item.get_rect(topleft=(50, 40))
                    msg_surface.blit(found_item, (50, 40))
                    add_option = text.render('Add it', True, WHITE)
                    add_option_rect = add_option.get_rect(topleft=(50, 80))
                    msg_surface.blit(add_option, (50, 80))
                    discard_option = text.render('Discard it', True, WHITE)
                    discard_option_rect = discard_option.get_rect(topleft=(50, 120))
                    msg_surface.blit(discard_option, (50, 120))
                    msg_surface_rect = msg_surface.get_rect(topleft=(80, 170))
                    window.blit(msg_surface, (80, 170))
                    pygame.display.update(msg_surface_rect)
                    if add_option_rect.collidepoint(mouse_pos[0] - 80,
                                                    mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (1, 0, 0):
                        if random_item.item_type == 'Weapon upgrade' and replace_weapon is True:
                            player_inventory.replace_item(random_item, player_inventory.items[0])
                        else:
                            player_inventory.add_item(random_item)
                        found_items_rect_index = pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif discard_option_rect.collidepoint(mouse_pos[0] - 80,
                                                          mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        found_items_rect_index = pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                elif random_item.item_type == 'Weapon upgrade':
                    found_item = text.render('You found a ' + random_item.item_name + ' (power lvl: ' + str(
                        random_item.item_power) + '). Use it as your main weapon? Current weapon power lvl: ' + str(
                        weapon_power), True, WHITE)
                    found_item_rect = found_item.get_rect(topleft=(50, 40))
                    msg_surface.blit(found_item, (50, 40))
                    add_option = text.render('Use it', True, WHITE)
                    add_option_rect = add_option.get_rect(topleft=(50, 80))
                    msg_surface.blit(add_option, (50, 80))
                    discard_option = text.render('Discard it', True, WHITE)
                    discard_option_rect = discard_option.get_rect(topleft=(50, 120))
                    msg_surface.blit(discard_option, (50, 120))
                    msg_surface_rect = msg_surface.get_rect(topleft=(80, 170))
                    window.blit(msg_surface, (80, 170))
                    pygame.display.update(msg_surface_rect)
                    if add_option_rect.collidepoint(mouse_pos[0] - 80,
                                                    mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (1, 0, 0):
                        if random_item.item_type == 'Weapon upgrade' and replace_weapon is True:
                            player_inventory.replace_item(random_item, player_inventory.items[0])
                        else:
                            player_inventory.add_item(random_item)
                        found_items_rect_index = pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif discard_option_rect.collidepoint(mouse_pos[0] - 80,
                                                          mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        found_items_rect_index = pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                else:
                    found_item = text.render('You found a ' + random_item.item_name + ' (Power: ' + str(
                        random_item.item_power) + '), but your inventory is full. Replace it with something?', True,
                                             WHITE)
                    found_item_rect = found_item.get_rect(topleft=(50, 40))
                    msg_surface.blit(found_item, (50, 40))
                    replace_option1 = text.render('Replace it with ' + player_inventory.items[0].item_name, True, WHITE)
                    replace_option1_rect = replace_option1.get_rect(topleft=(50, 80))
                    msg_surface.blit(replace_option1, (50, 80))
                    replace_option2 = text.render('Replace it with ' + player_inventory.items[1].item_name, True, WHITE)
                    replace_option2_rect = replace_option1.get_rect(topleft=(50, 120))
                    msg_surface.blit(replace_option2, (50, 120))
                    replace_option3 = text.render('Replace it with ' + player_inventory.items[2].item_name, True, WHITE)
                    replace_option3_rect = replace_option1.get_rect(topleft=(50, 160))
                    msg_surface.blit(replace_option3, (50, 160))
                    discard_option = text.render('Discard it', True, WHITE)
                    discard_option_rect = discard_option.get_rect(topleft=(50, 200))
                    msg_surface.blit(discard_option, (50, 200))
                    msg_surface_rect = msg_surface.get_rect(topleft=(80, 170))
                    window.blit(msg_surface, (80, 170))
                    pygame.display.update(msg_surface_rect)
                    if replace_option1_rect.collidepoint(mouse_pos[0] - 80,
                                                         mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        player_inventory.replace_item(random_item, player_inventory.items[0])
                        found_items_rect_index = pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif replace_option2_rect.collidepoint(mouse_pos[0] - 80,
                                                           mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        player_inventory.replace_item(random_item, player_inventory.items[1])
                        found_items_rect_index = pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif replace_option3_rect.collidepoint(mouse_pos[0] - 80,
                                                           mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        player_inventory.replace_item(random_item, player_inventory.items[2])
                        found_items_rect_index = pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif discard_option_rect.collidepoint(mouse_pos[0] - 80,
                                                          mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        found_items_rect_index = pygame.Rect(hero.x, hero.y, hero.width, hero.height).collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
            window.blit(map_tuple[map_ID].map_background, (0, 0))
            window.blit(entrance_img, drawn_map_entrance_rect)
            window.blit(exit_img, drawn_map_exit_rect)
            pygame.display.flip()

        # Update the display in each loop; try to make this more efficient
        msg_surface.fill(BLACK)
        window.blit(hero.load_img(), (hero.x, hero.y))
        new_opponents_rects = list()
        for o_rect in drawn_opponents_rects:
            new_o_pos = chase(o_rect[0], o_rect[1], hero.x, hero.y, drawn_wall_rects)
            new_o_rect = pygame.Rect(new_o_pos[0], new_o_pos[1], 64, 64)
            new_opponents_rects.append(new_o_rect)
        drawn_opponents_rects = new_opponents_rects
        for o_rect in drawn_opponents_rects:
            # if o_rect not in defeated_rects:
            window.blit(enemy1.load_img(), o_rect)
        onscreen_chars_rects.extend(new_opponents_rects)
        for i_rect in drawn_map_items_rects:
            if i_rect not in found_items_rects:
                window.blit(item_img, i_rect)
        window.blit(entrance_img, drawn_map_entrance_rect)
        window.blit(exit_img, drawn_map_exit_rect)
        msg_surface_rect = msg_surface.get_rect(topleft=(80, 170))
        pygame.display.update(drawn_map_entrance_rect)
        pygame.display.update(drawn_map_exit_rect)
        pygame.display.update(msg_surface_rect)
        pygame.display.update(drawn_wall_rects)
        pygame.display.update(onscreen_chars_rects)

    pygame.quit()
