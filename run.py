# Main game program


from battle import arena
from inventory import *
from maps import *
from profiles import hero

pygame.init()

if __name__ == "__main__":

    # Present the title screen and launch the game by pressing Enter or left-click

    title_screen = True
    soundtrack.load(track1)
    soundtrack.play(-1)
    while title_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pressed_keys = pygame.key.get_pressed()
        window.blit(title_img, (160, 113))
        pygame.display.flip()
        if pressed_keys[pygame.K_RETURN] or pygame.mouse.get_pressed() == (1, 0, 0):
            soundtrack.stop()
            window.fill(BLACK)
            pygame.display.flip()
            title_screen = False

    # Launch game and set initial variables

    run_game = True

    msg_surface_rect = msg_surface.get_rect(topleft=(80, 170))
    soundtrack.load(map_tuple[map_id].map_music)
    soundtrack.play(-1)
    defeated = []
    found_items_rects = []

    drawn_map = map_tuple[map_id]
    drawn_opponents = drawn_map.opponents
    wall_collision_index = -1
    test_hero_x = 0
    test_hero_y = 0
    last_direction_x = 0
    last_direction_y = 0
    last_wander = 0
    blink = False
    blink_timer = 0
    blink_length = random.randint(3600, 18000)
    blink_wait_timer = 0
    blink_wait_length = random.randint(3600, 18000)

    player_inventory = Backpack(None, 3)

    # Function to update the screen, with moving characters

    def display_update(dir_x, dir_y, lst_wander, blink_check):

        msg_surface.fill(BLACK)
        window.blit(map_tuple[map_id].map_background, (0, 0))
        window.blit(entrance_img, drawn_map_entrance_rect)
        window.blit(exit_img, drawn_map_exit_rect)
        wall_surface.blit(wall1, (0, 0))
        chase_results = ()
        for w_rect in drawn_wall_rects:
            window.blit(wall_surface, w_rect)
        for item in drawn_map_items:
            item_rect = pygame.Rect(item, (64, 64))
            if item_rect not in found_items_rects:
                window.blit(item_img, item_rect)
        window.blit(hero.surface, hero.rect)
        for op in drawn_opponents:
            chase_results = chase(op.rect[0], op.rect[1], hero.rect.x, hero.rect.y, drawn_wall_rects,
                                  dir_x, dir_y, lst_wander)
            new_o_pos = (chase_results[0], chase_results[1])
            if blink_check:
                blink_surface.set_alpha(100)
                if op not in defeated:
                    op.rect = pygame.Rect(new_o_pos, (64, 64))
                    window.blit(op.surface, op.rect)
            else:
                blink_surface.set_alpha(0)
        window.blit(blink_surface, (0, 0))
        pygame.display.flip()
        return chase_results[2], chase_results[3], chase_results[4]

    while run_game:

        framerate.tick(60)
        hero.speed = 10

        # Listen for the window being closed and quit the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        # Check what key is pressed in the current iteration of the game loop

        pressed_keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Redraw the map, characters and objects in each loop, to pick up changes

        drawn_map = map_tuple[map_id]
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
        drawn_map_items = drawn_map.map_items_pos

        last_direction_x = display_update(last_direction_x, last_direction_y, last_wander, blink)[0]
        last_direction_y = display_update(last_direction_x, last_direction_y, last_wander, blink)[1]
        last_wander = display_update(last_direction_x, last_direction_y, last_wander, blink)[2]

        # Run 'blinks' randomly

        if blink_timer <= blink_length and blink_wait_timer > blink_wait_length:
            blink = True
            blink_timer += 1
        elif blink_timer > blink_length and blink_wait_timer > blink_wait_length:
            blink = True
            blink_wait_timer = 0
            blink_wait_length = random.randint(3600, 18000)
            blink_timer += 1
        elif blink_timer <= blink_length and blink_wait_timer <= blink_wait_length:
            blink = False
            blink_wait_timer += 1
        elif blink_timer > blink_length and blink_wait_timer < blink_wait_length:
            blink = False
            blink_timer = 0
            blink_length = random.randint(3600, 18000)
            blink_wait_timer += 1

        # Check for keyboard input and test the proposed movement fits the boundaries of the window and map wall layout

        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_RIGHT] or \
                pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_DOWN]:
            while hero.speed > 0:
                if pressed_keys[pygame.K_LEFT]:
                    test_hero_x = hero.rect.x - hero.speed
                    test_hero_y = hero.rect.y
                if pressed_keys[pygame.K_RIGHT]:
                    test_hero_x = hero.rect.x + hero.speed
                    test_hero_y = hero.rect.y
                if pressed_keys[pygame.K_UP]:
                    test_hero_x = hero.rect.x
                    test_hero_y = hero.rect.y - hero.speed
                if pressed_keys[pygame.K_DOWN]:
                    test_hero_x = hero.rect.x
                    test_hero_y = hero.rect.y + hero.speed
                wall_collision_index = pygame.Rect(
                    test_hero_x, test_hero_y, hero.width, hero.height).collidelist(drawn_wall_rects)
                if wall_collision_index == -1:
                    if pressed_keys[pygame.K_LEFT] and hero.rect.x - hero.speed >= 0:
                        hero.rect.x -= hero.speed
                        break
                    elif pressed_keys[pygame.K_RIGHT] and hero.rect.x + hero.width + hero.speed <= window_width:
                        hero.rect.x += hero.speed
                        break
                    elif pressed_keys[pygame.K_UP] and hero.rect.y - hero.speed >= 0:
                        hero.rect.y -= hero.speed
                        break
                    elif pressed_keys[pygame.K_DOWN] and hero.rect.y + hero.height + hero.speed <= window_height:
                        hero.rect.y += hero.speed
                        break
                    else:
                        hero.speed -= 1
                else:
                    hero.speed -= 1
            old_map_id = map_id
            map_id, hero.rect.x, hero.rect.y, new_opponents = map_change_check(
                hero, map_id, drawn_map_entrance_rect, drawn_map_exit_rect)
            if map_id != old_map_id:
                drawn_opponents = new_opponents
                display_update(last_direction_x, last_direction_y, last_wander, blink)

        # Check for collisions between player and opponents to start a battle

        if blink:
            for op_test in drawn_opponents:
                if hero.rect.colliderect(op_test.rect) and op_test not in defeated:
                    defeated.append(op_test)
                    soundtrack.stop()
                    soundtrack.load(track3)
                    soundtrack.set_volume(0.4)
                    soundtrack.play(-1)
                    run_game = arena(hero, op_test, player_inventory)
                    soundtrack.stop()
                    soundtrack.set_volume(0.9)
                    soundtrack.load(drawn_map.map_music)
                    soundtrack.play(-1)

        # Item pickup and storage handling

        i0 = min(0, len(player_inventory.items) - 1)
        i1 = min(1, len(player_inventory.items) - 1)
        i2 = min(2, len(player_inventory.items) - 1)
        i3 = min(3, len(player_inventory.items) - 1)
        i4 = min(4, len(player_inventory.items) - 1)
        i5 = min(5, len(player_inventory.items) - 1)
        backpack_add_once = True

        for item_test in drawn_map_items:
            item_test_rect = pygame.Rect(item_test, (64, 64))
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

                    elif random_item.item_type == 'Weapon upgrade':
                        if player_inventory.held_weapon is not None:
                            weapon_power = player_inventory.held_weapon.item_power
                        else:
                            weapon_power = 0
                        found_item_text = text.render('You found a ' + random_item.item_name + ' (power lvl: ' + str(
                            random_item.item_power) + '). Use it as your main weapon? Current weapon power lvl: ' +
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

                    elif random_item.item_name != 'New Backpack' and random_item.item_type != 'Weapon upgrade' and \
                            len(player_inventory.items) < player_inventory.item_capacity:
                        found_item_text = text.render('You found a ' + random_item.item_name + ' (power lvl: ' + str(
                            random_item.item_power) + '). Add it to your inventory?', True, WHITE)
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
                            random_item.item_power) + '), but your inventory is full. Replace it with something?', True,
                                                      WHITE)
                        discard_option = text.render('Discard it', True, WHITE)
                        discard_option_rect = discard_option.get_rect(topleft=(50, 80))
                        msg_surface.blit(discard_option, (50, 80))
                        replace_option1 = text.render('Replace it with ' + player_inventory.items[i0].item_name, True,
                                                      WHITE)
                        replace_option1_rect = replace_option1.get_rect(topleft=(50, 120))
                        if len(player_inventory.items) >= 1:
                            msg_surface.blit(replace_option1, (50, 120))
                        replace_option2 = text.render('Replace it with ' + player_inventory.items[i1].item_name, True,
                                                      WHITE)
                        replace_option2_rect = replace_option2.get_rect(topleft=(50, 160))
                        if len(player_inventory.items) >= 2:
                            msg_surface.blit(replace_option2, (50, 160))
                        replace_option3 = text.render('Replace it with ' + player_inventory.items[i2].item_name, True,
                                                      WHITE)
                        replace_option3_rect = replace_option3.get_rect(topleft=(50, 200))
                        if len(player_inventory.items) >= 3:
                            msg_surface.blit(replace_option3, (50, 200))
                        replace_option4 = text.render('Replace it with ' + player_inventory.items[i3].item_name, True,
                                                      WHITE)
                        replace_option4_rect = replace_option4.get_rect(topleft=(50, 240))
                        if len(player_inventory.items) >= 4:
                            msg_surface.blit(replace_option4, (50, 240))
                        replace_option5 = text.render('Replace it with ' + player_inventory.items[i4].item_name, True,
                                                      WHITE)
                        replace_option5_rect = replace_option5.get_rect(topleft=(50, 280))
                        if len(player_inventory.items) >= 5:
                            msg_surface.blit(replace_option5, (50, 280))
                        replace_option6 = text.render('Replace it with ' + player_inventory.items[i5].item_name, True,
                                                      WHITE)
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
