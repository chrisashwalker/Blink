# Main game program


from battle import arena
from inventory import *
from maps import *
from profiles import hero

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
        window.blit(title_img, (160, 113))
        pygame.display.flip()
        if pressed_keys[pygame.K_RETURN] or pygame.mouse.get_pressed() == (1, 0, 0):
            soundtrack.stop()
            window.fill(BLACK)
            pygame.display.flip()
            title_screen = False

    run_game = True

    msg_surface_rect = msg_surface.get_rect(topleft=(80, 170))
    soundtrack.load(map_tuple[map_id].map_music)
    soundtrack.play(-1)
    defeated = []
    found_items_rects = []

    drawn_map = map_tuple[map_id]
    drawn_opponents = drawn_map.opponents
    wall_collision_index = -1

    player_inventory = Backpack(None, 3)


    def display_update():

        msg_surface.fill(BLACK)
        window.blit(map_tuple[map_id].map_background, (0, 0))
        window.blit(entrance_img, drawn_map_entrance_rect)
        window.blit(exit_img, drawn_map_exit_rect)
        wall_surface.blit(wall1, (0, 0))
        for w_rect in drawn_wall_rects:
            window.blit(wall_surface, w_rect)
        for i_rect in drawn_map_items_rects:
            if i_rect not in found_items_rects:
                window.blit(item_img, i_rect)
        window.blit(hero.surface, hero.rect)
        for op in drawn_opponents:
            new_o_pos = chase(op.rect[0], op.rect[1], hero.rect.x, hero.rect.y, drawn_wall_rects)
            op.rect = pygame.Rect(new_o_pos, (64, 64))
            if op not in defeated:
                window.blit(op.surface, op.rect)
        pygame.display.flip()


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
        drawn_map_items_rects = drawn_map.map_items_rects

        display_update()

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
                display_update()


        # Update rects based on character positions, check for collisions and start battle

        for op_test in drawn_opponents:
            if hero.rect.colliderect(op_test.rect) and op_test not in defeated:
                defeated.append(op_test)
                soundtrack.stop()
                soundtrack.load(track3)
                soundtrack.play(-1)
                run_game = arena(hero, op_test, player_inventory)
                soundtrack.stop()
                soundtrack.load(drawn_map.map_music)
                soundtrack.play(-1)

        # Item pickup handling

        if hero.rect.collidelist(drawn_map_items_rects) != -1 and \
                hero.rect.collidelist(found_items_rects) == -1:
            wait = True
            if player_inventory.item_capacity >= 6:
                items_tuple.remove(new_backpack)
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
                        random_item.item_type != 'Weapon upgrade' and random_item.item_name != 'New Backpack':
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
                        found_items_rect_index = hero.rect.collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif discard_option_rect.collidepoint(mouse_pos[0] - 80,
                                                          mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        found_items_rect_index = hero.rect.collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                elif random_item.item_type == 'Weapon upgrade':
                    found_item = text.render('You found a ' + random_item.item_name + ' (power lvl: ' + str(
                        random_item.item_power) + '). Use it as your main weapon? Current weapon power lvl: ' +
                                             str(player_inventory.held_weapon.item_power), True, WHITE)
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
                            player_inventory.held_weapon = random_item
                        else:
                            player_inventory.held_weapon = random_item
                        found_items_rect_index = hero.rect.collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif discard_option_rect.collidepoint(mouse_pos[0] - 80,
                                                          mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        found_items_rect_index = hero.rect.collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                elif random_item.item_name == 'New Backpack':
                    found_item = text.render(
                        'You found a ' + random_item.item_name + '. ' + random_item.item_type, True, WHITE)
                    found_item_rect = found_item.get_rect(topleft=(50, 40))
                    msg_surface.blit(found_item, (50, 40))
                    pygame.display.update(msg_surface_rect)
                    player_inventory.item_capacity += 1
                    found_items_rect_index = hero.rect.collidelist(
                        drawn_map_items_rects)
                    found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                    if pygame.mouse.get_pressed() == (1, 0, 0):
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
                        found_items_rect_index = hero.rect.collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif replace_option2_rect.collidepoint(mouse_pos[0] - 80,
                                                           mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        player_inventory.replace_item(random_item, player_inventory.items[1])
                        found_items_rect_index = hero.rect.collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif replace_option3_rect.collidepoint(mouse_pos[0] - 80,
                                                           mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        player_inventory.replace_item(random_item, player_inventory.items[2])
                        found_items_rect_index = hero.rect.collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False
                    elif discard_option_rect.collidepoint(mouse_pos[0] - 80,
                                                          mouse_pos[1] - 170) and pygame.mouse.get_pressed() == (
                            1, 0, 0):
                        found_items_rect_index = hero.rect.collidelist(
                            drawn_map_items_rects)
                        found_items_rects.append(pygame.Rect(drawn_map_items_rects[found_items_rect_index]))
                        wait = False

    pygame.quit()
