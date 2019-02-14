#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import database_interface as dbi

item_attributes_list = []

for i in range(100):
    item_attributes = {'name': 'Name' + str(i+1),
                       'function': 'Function' + str(i+1),
                       'weight': 0,
                       'volume': 0,
                       'price': 0,
                       'amount': 0}

    item_attributes_list.append(item_attributes)


def compare_item_data(item_tuple, attribute_dict, item_id=0):
    if item_id == 0:
        item_id = item_tuple[0]

    return item_tuple == (item_id,
                          attribute_dict['name'],
                          attribute_dict['function'],
                          attribute_dict['weight'],
                          attribute_dict['volume'],
                          attribute_dict['price'],
                          attribute_dict['amount'])


def test_initialize_db():
    db = dbi.Database(':memory:')
    db.initialize_db()

    # Test if calling initialization twice breaks the application
    db.initialize_db()

    # Test if the initialization added the table "items"
    with db.conn:
        db.cursor.execute(""" SELECT * FROM items """)
        assert len(db.cursor.fetchall()) == 0


def test_store_new_item_in_db():
    db = dbi.Database(':memory:')
    db.initialize_db()

    # Test if the an item was added
    db.store_new_item_in_db(item_attributes_list[0])
    with db.conn:
        db.cursor.execute(""" SELECT * FROM items """)
        item_list = db.cursor.fetchall()
        assert len(item_list) == 1
    assert compare_item_data(item_list[0], item_attributes_list[0])


def test_store_new_items_in_db_multiple_items():
    db = dbi.Database(':memory:')
    db.initialize_db()
    n_items = len(item_attributes_list)

    # Add multiple items into the database
    for i in range(n_items):
        db.store_new_item_in_db(item_attributes_list[i])
    # Fetch items from database
    with db.conn:
        db.cursor.execute(""" SELECT * FROM items """)
        item_list = db.cursor.fetchall()
    # Test if all items have been correctly added
    assert len(item_list) == n_items
    for i in range(n_items):
        assert compare_item_data(item_list[i], item_attributes_list[i], i+1)


def test_utf8_support():
    # For sqlite not needed - found online:
    # "By default, pysqlite decodes all strings to Unicode,
    # assuming UTF-8 encoding (which SQLite assumes when parsing statements)."
    pass
