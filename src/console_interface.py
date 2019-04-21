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
__version__ = "0.0.1"
__license__ = "MIT"

db_name = ':memory:'

default_values_new_item = {'name': "Name",
                           'function': "Function",
                           'weight': "0",
                           'volume': "0",
                           'price': "0",
                           'amount': "0"}


class AddItem(nps.ActionFormV2):
    """
    Screen containing a formular to enter the attributes of a new item.
    It has an 'OK' button which saves the new item in the database and
    a 'CANCEL' button to leave the formular without changing the database.
    """
    def create(self):
        """
        Draws the formular with fields to enter the attributes.
        Fills the field with default values.
        """
        # draw the fields needed to enter the attributes
        self._name = self.add(nps.TitleText, name="name: ")
        self._function = self.add(nps.TitleText, name="function: ")
        self._weight = self.add(nps.TitleText, name="weight: ")
        self._volume = self.add(nps.TitleText, name="volume: ")
        self._price = self.add(nps.TitleText, name="price: ")
        self._amount = self.add(nps.TitleText, name="amount: ")

        # fill in the fields with the default values
        self._name.value = default_values_new_item['name']
        self._function.value = default_values_new_item['function']
        self._weight.value = default_values_new_item['weight']
        self._volume.value = default_values_new_item['volume']
        self._price.value = default_values_new_item['price']
        self._amount.value = default_values_new_item['amount']

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
        self.parentApp.db.store_new_item_in_db(item_data)

        # reset to default entries for next time the formular it is used
        self._name.value = default_values_new_item['name']
        self._function.value = default_values_new_item['function']
        self._weight.value = default_values_new_item['weight']
        self._volume.value = default_values_new_item['volume']
        self._price.value = default_values_new_item['price']
        self._amount.value = default_values_new_item['amount']

    def on_cancel(self):
        """
        Gets called when the 'CANCEL' button is pressed.
        Make no changes to the database and exit the formular.
        """
        self.parentApp.setNextForm(None)
        pass


class App(nps.NPSAppManaged):
    def onStart(self):
        # add an abstract database object to the application
        # used by user interface to make changes to the database
        self.db = dbi.Database(self.db_name)

        # add the different screens to the application
        # 'MAIN' is the starting screen
        self.add_item = self.addForm('MAIN',
                                     AddItem,
                                     name="Add a new Item")


if __name__ == "__main__":
    """
    Runs the application and connects the user interface to the database.
    """
    app = App()
    app.db_name = db_name
    app = app.run()
