#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Docstring
"""
import npyscreen as nps
import DatabaseInterface as dbi

__author__ = "Marco Zeller"
__version__ = "0.0.0"
__license__ = "MIT"


class AddItem(nps.ActionFormV2):
    def create(self):
        self._name = self.add(nps.TitleText, name="name: ")
        self._function = self.add(nps.TitleText, name="function: ")
        self._weight = self.add(nps.TitleText, name="weight: ")
        self._volume = self.add(nps.TitleText, name="volume: ")
        self._price = self.add(nps.TitleText, name="price: ")
        self._amount = self.add(nps.TitleText, name="amount: ")

        self._name.value = "Test1"
        self._function.value = "Function"
        self._weight.value = "0"
        self._volume.value = "0"
        self._price.value = "0"
        self._amount.value = "0"

    def on_ok(self):
        item_data = {}
        item_data['name'] = self._name.value
        item_data['function'] = self._function.value
        item_data['weight'] = int(self._weight.value)
        item_data['volume'] = int(self._volume.value)
        item_data['price'] = int(self._price.value)
        item_data['amount'] = int(self._amount.value)

        self.parentApp.db.store_new_item_in_db(item_data)

    def on_cancel(self):
        pass

    def afterEditing(self):
        self.parentApp.setNextForm('MAIN')


class App(nps.NPSAppManaged):
    def onStart(self):
        self.db = dbi.Database(':memory:')
        self.add_item = self.addForm('MAIN',
                                     AddItem,
                                     name="Add a new Item")


if __name__ == "__main__":
    """ TODO: """
    app = App().run()
