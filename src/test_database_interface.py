#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import database_interface as dbi

# Produce some test data:
n_items = 100
item_attributes_list = n_items*[None]

for i in range(n_items):
    item_attributes = {'name': 'Name' + str(i+1),
                       'function': 'Function' + str(i+1),
                       'weight': 0,
                       'volume': 0,
                       'price': 0,
                       'amount': 0}

    item_attributes_list[i] = (item_attributes)


def compare_item_data(item_tuple, attribute_dict, item_id=0):
    """
    Helper function used to compare an item tuple
    as it comes out of the database with an atribute dictionary
    as it is used internally by the program to communicate between interfaces.
    Optionally the internally used item_id can be given as a separate argument.
    If no item_id is given (or the given item_id has value 0)
    only the attributes are compared.
    """
    if item_id == 0:
        item_id = item_tuple[0]

    return item_tuple == (item_id,
                          attribute_dict['name'],
                          attribute_dict['function'],
                          attribute_dict['weight'],
                          attribute_dict['volume'],
                          attribute_dict['price'],
                          attribute_dict['amount'])


def test_initialize():
    db = dbi.Database(':memory:')
    db.initialize()

    # Test if calling initialization twice breaks the application
    db.initialize()

    # Test if the initialization added the table "items"
    with db.conn:
        db.cursor.execute(""" SELECT * FROM items """)
        assert len(db.cursor.fetchall()) == 0


def test_store_new_item():
    db = dbi.Database(':memory:')
    db.initialize()

    # Test if the an item was added
    db.store_new_item(item_attributes_list[0])
    with db.conn:
        db.cursor.execute(""" SELECT * FROM items """)
        item_list = db.cursor.fetchall()
        assert len(item_list) == 1
    assert compare_item_data(item_list[0], item_attributes_list[0])


def test_store_new_item_multiple_items():
    db = dbi.Database(':memory:')
    db.initialize()

    # Add multiple items into the database
    for i in range(n_items):
        db.store_new_item(item_attributes_list[i])
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


def compare_item_dicts(attribute_dict1, attribute_dict2):
    """
    Helper function used to compare two attribute dictionaries.
    Returns true if they have the same attributes return false otherwise.
    """
    return attribute_dict1['name'] == attribute_dict2['name'] and \
        attribute_dict1['function'] == attribute_dict2['function'] and \
        attribute_dict1['weight'] == attribute_dict2['weight'] and \
        attribute_dict1['volume'] == attribute_dict2['volume'] and \
        attribute_dict1['price'] == attribute_dict2['price'] and \
        attribute_dict1['amount'] == attribute_dict2['amount']


def test_get_all_items():
    db = dbi.Database(':memory:')
    db.initialize()

    # Add multiple items into the database
    for i in range(n_items):
        db.store_new_item(item_attributes_list[i])
    # Fetch items from database
    item_list = db.get_all_items()
    # Test if all items have been correctly added
    assert len(item_list) == n_items
    # TODO: sort the lists before comparing its elements
    #       since the database does not need to guarantee
    #       to return the values in a specific order.
    for i in range(n_items):
        assert compare_item_dicts(item_list[i], item_attributes_list[i])


def test_update_item():
    db = dbi.Database(':memory:')
    db.initialize()

    # Add multiple items into the database
    for i in range(n_items):
        db.store_new_item(item_attributes_list[i])

    modified_item_list = 100*[None]
    for i in range(100):
        item_attributes = {'id': i+1,
                           'name': 'NewName' + str(i+1),
                           'function': 'NewFunction' + str(i+1),
                           'weight': i+1,
                           'volume': i+1,
                           'price': i+1,
                           'amount': i+1}
        db.update_item(item_attributes)
        modified_item_list[i] = item_attributes

    # Fetch items from database
    item_list = db.get_all_items()

    # Test if the exact number of items are beeing read from database
    assert len(item_list) == n_items
    assert len(item_list) == len(modified_item_list)
    # TODO: sort the lists before comparing its elements
    #       since the database does not need to guarantee
    #       to return the values in a specific order.
    for i in range(n_items):
        assert not compare_item_dicts(item_list[i], item_attributes_list[i])
        assert compare_item_dicts(item_list[i], modified_item_list[i])


def test_delete_item():
    # TODO: implement this test
    pass


def test_store_new_pack():
    # TODO: implement this test
    pass


def test_get_all_packs():
    # TODO: implement this test
    pass


def test_get_attributes_pack():
    # TODO: implement this test
    pass


def test_get_items_in_pack():
    # TODO: implement this test
    pass


def test_get_items_not_in_pack():
    # TODO: implement this test
    pass
