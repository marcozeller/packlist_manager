#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Docstring
"""
import npyscreen as nps
import database_interface as dbi

__author__ = "Marco Zeller"
__version__ = "0.0.0"
__license__ = "MIT"

db_name = ':memory:'

default_values_new_item = {'name': "Name",
                           'function': "Function",
                           'weight': "0",
                           'volume': "0",
                           'price': "0",
                           'amount': "0"}


class AddItem(nps.ActionFormV2):
    def create(self):
        self._name = self.add(nps.TitleText, name="name: ")
        self._function = self.add(nps.TitleText, name="function: ")
        self._weight = self.add(nps.TitleText, name="weight: ")
        self._volume = self.add(nps.TitleText, name="volume: ")
        self._price = self.add(nps.TitleText, name="price: ")
        self._amount = self.add(nps.TitleText, name="amount: ")

        self._name.value = default_values_new_item['name']
        self._function.value = default_values_new_item['function']
        self._weight.value = default_values_new_item['weight']
        self._volume.value = default_values_new_item['volume']
        self._price.value = default_values_new_item['price']
        self._amount.value = default_values_new_item['amount']

    def on_ok(self):
        item_data = {}
        item_data['name'] = self._name.value
        item_data['function'] = self._function.value
        item_data['weight'] = int(self._weight.value)
        item_data['volume'] = int(self._volume.value)
        item_data['price'] = int(self._price.value)
        item_data['amount'] = int(self._amount.value)

        self.parentApp.db.store_new_item_in_db(item_data)

        self._name.value = default_values_new_item['name']
        self._function.value = default_values_new_item['function']
        self._weight.value = default_values_new_item['weight']
        self._volume.value = default_values_new_item['volume']
        self._price.value = default_values_new_item['price']
        self._amount.value = default_values_new_item['amount']

    def on_cancel(self):
        self.parentApp.setNextForm(None)
        pass


class App(nps.NPSAppManaged):
    def onStart(self):
        self.db = dbi.Database(self.db_name)
        self.add_item = self.addForm('MAIN',
                                     AddItem,
                                     name="Add a new Item")


if __name__ == "__main__":
    """ TODO: """
    app = App()
    app.db_name = db_name
    app = app.run()
