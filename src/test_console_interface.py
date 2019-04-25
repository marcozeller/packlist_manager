#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import curses
import npyscreen as nps
import console_interface as coi
import test_database_interface as tdi

"""
nps.TEST_SETTINGS = {
    'TEST_INPUT': None,
    'TEST_INPUT_LOG': [],
    'CONTINUE_AFTER_TEST_INPUT': False,
    'INPUT_GENERATOR': False
}
"""

nps.TEST_SETTINGS['TEST_INPUT'] = []
nps.TEST_SETTINGS['CONTINUE_AFTER_TEST_INPUT'] = False

test_item = {'name': "TestName",
             'function': "TestFunction",
             'weight': 1,
             'volume': 2,
             'price': 3,
             'amount': 4}


def insert_item_values_in_fields(item_values):
    # delete the default values by pressing backspace as many times as
    # there are characters in default value
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        coi.default_values_new_item['name']]
    # then enter the item's corresponding value
    nps.TEST_SETTINGS['TEST_INPUT'] += item_values['name']
    # go to the next field
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        coi.default_values_new_item['function']]
    nps.TEST_SETTINGS['TEST_INPUT'] += item_values['function']
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        coi.default_values_new_item['weight']]
    nps.TEST_SETTINGS['TEST_INPUT'] += str(item_values['weight'])
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        coi.default_values_new_item['volume']]
    nps.TEST_SETTINGS['TEST_INPUT'] += str(item_values['volume'])
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        coi.default_values_new_item['price']]
    nps.TEST_SETTINGS['TEST_INPUT'] += str(item_values['price'])
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        coi.default_values_new_item['amount']]
    nps.TEST_SETTINGS['TEST_INPUT'] += str(item_values['amount'])


def test_insert_item_via_console_interface():
    # go to add item screen from main menu
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    # add the item values and press enter
    insert_item_values_in_fields(test_item)
    # go to the 'OK' button and press enter to save and get to main menu
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_RIGHT]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    # go down in the main menu and press 'OK' to save and exit the program
    nps.TEST_SETTINGS['TEST_INPUT'] += 4*[curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work
    # TODO: Read from database and compare as soon as implemented!
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()

    assert len(item_list) == 1
    assert tdi.compare_item_data(item_list[0], test_item)


def test_cancel_button_insert_item_via_console_interface():
    """
    Add testcase to check if the cancel button works correctly.
    """
    # go to add item screen from main menu
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    # add the item values and press enter
    insert_item_values_in_fields(test_item)
    # go to the 'CANCEL' button and press enter to go to main menu without saving
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    # go down in the main menu and press 'OK' to exit the program
    nps.TEST_SETTINGS['TEST_INPUT'] += 4*[curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()

    assert len(item_list) == 0


def test_insert_multiple_item_via_console_interface():
    for i in range(10):
        # go to add item screen from main menu
        nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10: code for the Enter Key
        # add the item values and press enter
        insert_item_values_in_fields(test_item)
        # go to the 'OK' button and press enter to save and get to main menu
        nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
        nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_RIGHT]
        nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10: code for the Enter Key

    # go down in the main menu and press 'CANCEL' to exit the program
    nps.TEST_SETTINGS['TEST_INPUT'] += 4*[curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work
    # TODO: Read from database and compare as soon as implemented!
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()
    assert len(item_list) == 10
    for i in range(10):
        assert tdi.compare_item_data(item_list[i], test_item)


def test_cancel_button_insert_multiple_item_via_console_interface():
    for i in range(10):
        # go to add item screen from main menu
        nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10: code for the Enter Key
        # add the item values and press enter
        insert_item_values_in_fields(test_item)
        # go to the 'CANCEL' button and press enter to save and get to main menu
        nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
        nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10: code for the Enter Key

    # go down in the main menu and press 'CANCEL' to exit the program
    nps.TEST_SETTINGS['TEST_INPUT'] += 4*[curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()
    assert len(item_list) == 0
