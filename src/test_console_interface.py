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
    # there are characters in default values
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        coi.default_values_new_item['name']]
    # then enter the item's corresponding value
    nps.TEST_SETTINGS['TEST_INPUT'] += item_values['name']
    # go to the next field and repeat
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


def go_to_add_item_screen_from_main_menu():
    """
    Go to add item screen from the main menu.
    """
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key


def press_ok_button_after_entering_values_in_add_item_screen():
    """
    Go to the 'OK' button and press enter to save and get to main menu.
    """
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_RIGHT]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key


def press_cancel_button_after_entering_values_in_add_item_screen():
    """
    Go to the 'CANCEL' button and press enter to save and get to main menu.
    """
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key


def press_ok_button_from_main_menu():
    """
    Go down in the main menu and press 'OK' to exit the program.
    """
    nps.TEST_SETTINGS['TEST_INPUT'] += 4*[curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key


def test_insert_item_via_console_interface():
    """
    Inserts a single item via the console-interface and check manually
    if it was added to the database.
    """
    go_to_add_item_screen_from_main_menu()

    insert_item_values_in_fields(test_item)

    press_ok_button_after_entering_values_in_add_item_screen()

    press_ok_button_from_main_menu()

    # run the test-input on the application
    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work

    # TODO: Read from database and compare as soon as implemented!
    # manually look into database to see if item has been correctly added
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()

    assert len(item_list) == 1
    assert tdi.compare_item_data(item_list[0], test_item)


def test_cancel_button_insert_item_via_console_interface():
    """
    Check if the cancel button in the add item screen works correctly.
    Inserts a single item into the console-interface and check manually
    that nothing was added to the database.
    """
    go_to_add_item_screen_from_main_menu()

    insert_item_values_in_fields(test_item)

    press_cancel_button_after_entering_values_in_add_item_screen()

    press_ok_button_from_main_menu()

    # run the test-input on the application
    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work

    # manually look into database to see check that no item has been added
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()

    assert len(item_list) == 0


def test_insert_multiple_item_via_console_interface():
    """
    Check if the cancel button in the add item screen works correctly.
    Inserts a several items via the console-interface and check manually
    that nothing was added to the database.
    """
    for i in range(10):
        go_to_add_item_screen_from_main_menu()

        insert_item_values_in_fields(test_item)

        press_ok_button_after_entering_values_in_add_item_screen()

    press_ok_button_from_main_menu()

    # run the test-input on the application
    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work

    # TODO: Read from database and compare as soon as implemented!
    # manually look into database to see if items have been added
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()
    assert len(item_list) == 10
    for i in range(10):
        assert tdi.compare_item_data(item_list[i], test_item)


def test_cancel_button_insert_multiple_item_via_console_interface():
    """
    Inserts several items via the console-interface and check manually
    if it was added to the database.
    """
    for i in range(10):
        go_to_add_item_screen_from_main_menu()

        insert_item_values_in_fields(test_item)

        press_cancel_button_after_entering_values_in_add_item_screen()

    press_ok_button_from_main_menu()

    # run the test-input on the application
    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work

    # manually look into database to see check that no item has been added
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()
    assert len(item_list) == 0
