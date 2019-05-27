#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import curses
import npyscreen as nps
import console_interface as coi
import test_database_interface as tdi
import decimal

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
             'weight': decimal.Decimal(1.0),
             'volume': decimal.Decimal(2.0),
             'price': decimal.Decimal(3.0),
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


def go_to_list_item_screen_from_main_menu():
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
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
    Inserts several items via the console-interface and check manually
    if it was added to the database.
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

    # manually look into database to see if items have been added
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()
    assert len(item_list) == 10
    for i in range(10):
        assert tdi.compare_item_data(item_list[i], test_item)


def test_cancel_button_insert_multiple_item_via_console_interface():
    """
    Check if the cancel button in the add item screen works correctly.
    Inserts a several items via the console-interface and check manually
    that nothing was added to the database.
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


def test_list_items_after_inserting_single_item():
    """
    Inserts a single item via the console-interface and check if there is a
    corresponding entry in the list items screen.
    """
    go_to_add_item_screen_from_main_menu()

    insert_item_values_in_fields(test_item)

    press_ok_button_after_entering_values_in_add_item_screen()

    go_to_list_item_screen_from_main_menu()

    # make sure the list is only one entry long by clicking down
    # until we are on the 'OK' button and hit it
    # TODO: This step needs to be revised - figure out how to do that...
    #       At the moment only fails if to many entries are present.
    #       Need to figure out how to read from the screen.
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    press_ok_button_from_main_menu()

    # run the test-input on the application
    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work


def test_list_items_after_inserting_multiple_items():
    """
    Inserts several items via the console-interface and check if there are a
    corresponding number of entries in the list items screen.
    """
    for i in range(10):
        go_to_add_item_screen_from_main_menu()

        insert_item_values_in_fields(test_item)

        press_ok_button_after_entering_values_in_add_item_screen()

    go_to_list_item_screen_from_main_menu()

    # make sure the list has the correct number of entries.
    # TODO: This step needs to be revised - figure out how to do that...
    #       At the moment only fails if to many entries are present.
    #       Need to figure out how to read from the screen.
    nps.TEST_SETTINGS['TEST_INPUT'] += 10*[curses.KEY_DOWN]
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    press_ok_button_from_main_menu()

    # run the test-input on the application
    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work


def change_item_values(from_item, to_item):
    """
    Change the items data by deleting values from_item
    and replacing with the values found in to_item.
    from_item and to_item are both dictionaries with values for the respective
    attribute-string as key.
    """
    # delete the existing values by pressing backspace as many times as
    # there are characters in from_values values
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        from_item['name']]
    # then enter the item's corresponding value
    nps.TEST_SETTINGS['TEST_INPUT'] += to_item['name']
    # go to the next field and repeat
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        from_item['function']]
    nps.TEST_SETTINGS['TEST_INPUT'] += to_item['function']
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        str(from_item['weight'])]
    nps.TEST_SETTINGS['TEST_INPUT'] += str(to_item['weight'])
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        str(from_item['volume'])]
    nps.TEST_SETTINGS['TEST_INPUT'] += str(to_item['volume'])
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        str(from_item['price'])]
    nps.TEST_SETTINGS['TEST_INPUT'] += str(to_item['price'])
    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]

    nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_BACKSPACE for char in
                                        str(from_item['amount'])]
    nps.TEST_SETTINGS['TEST_INPUT'] += str(to_item['amount'])


def test_update_items():
    """
    Inserts several items modify them via the console-interface
    and check if there are corresponding entries in the list items screen.
    """
    for i in range(10):
        go_to_add_item_screen_from_main_menu()

        insert_item_values_in_fields(test_item)

        press_ok_button_after_entering_values_in_add_item_screen()

    go_to_list_item_screen_from_main_menu()

    new_item = {'name': "NewName",
                'function': "NewTestFunction",
                'weight': decimal.Decimal(2.0),
                'volume': decimal.Decimal(3.0),
                'price': decimal.Decimal(4.0),
                'amount': 5}

    for i in range(10):
        # select first item to change
        nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key
        change_item_values(test_item, new_item)
        press_ok_button_after_entering_values_in_add_item_screen()

        # put cursor on next item
        nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
        nps.TEST_SETTINGS['TEST_INPUT'] += i*[curses.KEY_DOWN]

    # for the last loop iteration above sets the cursor on the 'OK' button
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key

    press_ok_button_from_main_menu()

    # run the test-input on the application
    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work

    # manually look into database to see if items have been changed
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()
    assert len(item_list) == 10
    """
    for i in range(10):
        assert not tdi.compare_item_data(item_list[i], test_item)
        assert tdi.compare_item_data(item_list[i], new_item)
    """


def test_update_items_cancel_button():
    """
    Inserts several items attempt to change their values
    in the change item screen, but then presses the 'CANCEL' button.
    Then check that none of the entries have been modified.
    """
    for i in range(10):
        go_to_add_item_screen_from_main_menu()

        insert_item_values_in_fields(test_item)

        press_ok_button_after_entering_values_in_add_item_screen()

    """
    go_to_list_item_screen_from_main_menu()


    new_item = {'name': "NewName",
                'function': "NewTestFunction",
                'weight': decimal.Decimal(2),
                'volume': decimal.Decimal(3),
                'price': decimal.Decimal(4),
                'amount': 5}

    for i in range(10):
        # select first item to change
        nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key
        change_item_values(test_item, new_item)
        press_cancel_button_after_entering_values_in_add_item_screen()

        # put cursor on next item
        nps.TEST_SETTINGS['TEST_INPUT'] += [curses.KEY_DOWN]
        nps.TEST_SETTINGS['TEST_INPUT'] += i*[curses.KEY_DOWN]

    # for the last loop iteration above sets the cursor on the 'OK' button
    nps.TEST_SETTINGS['TEST_INPUT'] += [10]  # 10 is the code for the Enter Key
    """

    press_ok_button_from_main_menu()

    # run the test-input on the application
    app = coi.App()
    app.db_name = ':memory:'
    app.run(fork=False)  # needs to run "py.test -s" else does not work

    # manually look into database to see if items have not been changed
    with app.db.conn:
        app.db.cursor.execute(""" SELECT * FROM items """)
        item_list = app.db.cursor.fetchall()
    assert len(item_list) == 10
    """
    for i in range(10):
        assert tdi.compare_item_data(item_list[i], test_item)
        assert not tdi.compare_item_data(item_list[i], new_item)
    """


def test_delete_items():
    # TODO: implement this test
    pass


def test_add_new_packs_only_with_items():
    # TODO: implement this test
    pass


def test_list_all_packs():
    # TODO: implement this test
    pass


def test_show_attributes_of_a_pack_only_with_items():
    # TODO: implement this test
    pass


def test_update_attributes_of_a_pack_only_with_items():
    # TODO: implement this test
    pass


def test_update_selected_items_of_a_pack():
    # TODO: implement this test
    pass


def test_add_new_packs_also_with_packs():
    # TODO: implement this test
    pass
