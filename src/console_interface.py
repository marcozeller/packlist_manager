#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Describes an interactive user interface running in the console
using npyscreen a library on top of ncurses.
This module uses the database interface module to interact with the database
and the utility module for more complex operations.
"""
import npyscreen as nps
import database_interface as dbi

__author__ = "Marco Zeller"
__version__ = "0.0.2"
__license__ = "MIT"

db_name = ':memory:'

default_values_new_item = {'name':     "Name",
                           'function': "Function",
                           'weight':   "0",
                           'volume':   "0",
                           'price':    "0",
                           'amount':   "0"}

language_english = {'name':         "Name: ",
                    'function':     "Function: ",
                    'weight':       "Weight: ",
                    'volume':       "Volume: ",
                    'price':        "Price: ",
                    'amount':       "Amount: ",
                    'main_menu':    "Main Menu",
                    'add_new_item': "Add a new Item",
                    'list_items':   "List Items",
                    'add_new_pack': "Add a new Pack",
                    'list_packs':   "List Packs"}

language = language_english


class MainMenu(nps.ActionFormMinimal):
    def go_to_add_item_screen(self):
        self.parentApp.switchForm('ADD_ITEM')

    def go_to_list_items_screen(self):
        self.parentApp.switchForm('LIST_ITEMS')

    def go_to_add_pack_screen(self):
        self.parentApp.switchForm('ADD_PACK')

    def go_to_list_packs_screen(self):
        self.parentApp.switchForm('LIST_PACKS')

    def create(self):
        self.add(nps.ButtonPress,
                 name=language['add_new_item'],
                 when_pressed_function=self.go_to_add_item_screen)
        self.add(nps.ButtonPress,
                 name=language['list_items'],
                 when_pressed_function=self.go_to_list_items_screen)
        self.add(nps.ButtonPress,
                 name=language['add_new_pack'],
                 when_pressed_function=self.go_to_add_pack_screen)
        self.add(nps.ButtonPress,
                 name=language['list_packs'],
                 when_pressed_function=self.go_to_list_packs_screen)

    def on_ok(self):
        self.parentApp.setNextForm(None)


class AddItem(nps.ActionFormV2):
    """
    Screen containing a formular to enter the attributes of a new item.
    It has an 'OK' button which saves the new item in the database and
    a 'CANCEL' button to leave the formular without changing the database.
    """
    def reset_fields(self):
        self._name.value = default_values_new_item['name']
        self._function.value = default_values_new_item['function']
        self._weight.value = default_values_new_item['weight']
        self._volume.value = default_values_new_item['volume']
        self._price.value = default_values_new_item['price']
        self._amount.value = default_values_new_item['amount']

    def create(self):
        """
        Draws the formular with fields to enter the attributes.
        Fills the field with default values.
        """
        # draw the fields needed to enter the attributes
        self._name = self.add(nps.TitleText, name=language['name'])
        self._function = self.add(nps.TitleText, name=language['function'])
        self._weight = self.add(nps.TitleText, name=language['weight'])
        self._volume = self.add(nps.TitleText, name=language['volume'])
        self._price = self.add(nps.TitleText, name=language['price'])
        self._amount = self.add(nps.TitleText, name=language['amount'])

        # fill in the fields with the default values
        self.reset_fields()

    def on_ok(self):
        """
        Gets called when the 'OK' button is pressed.
        Saves all the attributes into the database.
        """
        # create a dictionary containing the attributes of the new item
        item_data = {}
        item_data['name'] = self._name.value
        item_data['function'] = self._function.value
        item_data['weight'] = int(self._weight.value)
        item_data['volume'] = int(self._volume.value)
        item_data['price'] = int(self._price.value)
        item_data['amount'] = int(self._amount.value)

        # send the dictionary to the database interface
        self.parentApp.db.store_new_item(item_data)

        # reset to default entries for next time the formular it is used
        self.reset_fields()

        # go back to main screen
        self.parentApp.setNextForm('MAIN')

    def on_cancel(self):
        """
        Gets called when the 'CANCEL' button is pressed.
        Make no changes to the database and exit the formular.
        """
        # reset to default entries for next time the formular it is used
        self.reset_fields()

        # go back to main screen
        self.parentApp.setNextForm('MAIN')


class ItemList(nps.MultiLineAction):
    def display_value(self, vl):
        return str(vl['id']) + ': ' + vl['name']

    def actionHighlighted(self, act_on_this, keypress):
        pass
        # TODO:
        # self.parent.parentApp.selected_item = act_on_this
        # self.parent.parentApp.setNextForm('MAIN')


class ListItems(nps.ActionFormMinimal):
    def create(self):
        item_list = self.parentApp.db.get_all_items()
        self.item_list_widget = self.add(ItemList,
                                         values=item_list,
                                         scroll_exit=True,
                                         exit_right=True)

    def beforeEditing(self):
        self.item_list_widget.values = self.parentApp.db.get_all_items()

    def on_ok(self):
        self.parentApp.setNextForm('MAIN')


class App(nps.NPSAppManaged):
    def onStart(self):
        # add an abstract database object to the application
        # used by user interface to make changes to the database
        self.db = dbi.Database(self.db_name)

        # add the different screens to the application
        # 'MAIN' is the starting screen
        self.add_item = self.addForm('MAIN',
                                     MainMenu,
                                     name=language['main_menu'])
        self.add_item = self.addForm('ADD_ITEM',
                                     AddItem,
                                     name=language['add_new_item'])
        self.add_item = self.addForm('LIST_ITEMS',
                                     ListItems,
                                     name=language['list_items'])
        self.add_item = self.addForm('ADD_PACK',
                                     AddItem,
                                     name=language['add_new_pack'])
        self.add_item = self.addForm('LIST_PACKS',
                                     AddItem,
                                     name=language['list_packs'])


if __name__ == "__main__":
    """
    Runs the application and connects the user interface to the database.
    """
    app = App()
    app.db_name = db_name
    app = app.run()
