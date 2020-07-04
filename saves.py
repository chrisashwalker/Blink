import sqlite3


def save_game(
        user, level_no, held_weapon, inventory_capacity, inventory_items, found_items_pos, level_type, level_layout):
    # Connect to the saves database
    conn = sqlite3.connect('game_saves.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS saves
    (user text, level_no integer, held_weapon text, inventory_capacity integer, inventory_items text, 
    found_items_pos text, level_type integer, level_layout text)''')

    save_data = (
        user, level_no, held_weapon, inventory_capacity, inventory_items, found_items_pos, level_type, level_layout)

    # Get existing save data and overwrite the data if it exists, otherwise create a new database entry
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
        level_no = ?, held_weapon = ?, inventory_capacity = ?, 
        inventory_items = ?, found_items_pos = ?, level_type = ?, level_layout = ?
        WHERE
        user = ?
        ''', reordered_save_data)

    conn.commit()


def fetch_all_saves():
    conn = sqlite3.connect('game_saves.db')
    c = conn.cursor()

    c.execute('''SELECT user, level_no, held_weapon, inventory_capacity, 
    inventory_items, found_items_pos, level_type, level_layout
    FROM saves
    ''')

    all_saves = c.fetchall()

    return all_saves
