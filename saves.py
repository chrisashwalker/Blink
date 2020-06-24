import sqlite3


def save_game(user, held_weapon, inventory_capacity, inventory_items, map_id, hero_x, hero_y, found_items_pos):
    conn = sqlite3.connect('game_saves.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS saves
    (user text, held_weapon text, inventory_capacity integer, inventory_items text, map_id integer, 
    hero_x integer, hero_y integer, found_items_pos text)''')

    save_data = (user, held_weapon, inventory_capacity, inventory_items, map_id, hero_x, hero_y, found_items_pos)

    c.execute('''SELECT user FROM saves
    WHERE user = ?''', [save_data[0]])

    existing_save = c.fetchone()

    if existing_save is None:
        c.execute('''INSERT INTO saves
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', save_data)
    else:
        reordered_save_data = (
            save_data[1], save_data[2], save_data[3], save_data[4],
            save_data[5], save_data[6], save_data[7], save_data[0])
        c.execute('''UPDATE saves
        SET
        held_weapon = ?, inventory_capacity = ?, inventory_items = ?, 
        map_id = ?, hero_x = ?, hero_y = ?, found_items_pos = ?
        WHERE
        user = ?
        ''', reordered_save_data)

    conn.commit()


def fetch_all_saves():
    conn = sqlite3.connect('game_saves.db')
    c = conn.cursor()

    c.execute('''SELECT user, held_weapon, inventory_capacity, inventory_items, map_id, hero_x, hero_y, found_items_pos
    FROM saves
    ''')

    all_saves = c.fetchall()

    return all_saves
