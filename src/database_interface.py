#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module is used by the userinterfaces to interact with the database.
It offers abstractions for all the functionality provided by the database.
"""
import sqlite3


class Database:
    def __init__(self, db_name):
        """
        The argument db_name is a string, giving the name of the database
        in the filesystem.
        Use db_name = ':memory:' to create a temporary database for testing.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # initialize the database here to take the burden off the user
        self.initialize()

    def initialize(self):
        """
        Creates the tables needed for storing the data if
        they do not already exist.
        Needs be called before a new database can be used.
        If called on an existing database it does not have any side effects.
        """
        with self.conn:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS items(
                                   id integer primary key autoincrement,
                                   name text,
                                   function text,
                                   weight integer,
                                   volume integer,
                                   price integer,
                                   amount integer) """)

    def store_new_item(self, item_values):
        """
        Stores a new item in the database.
        item_values is a dict with the attribute's name (String) as key
        to the corresponding value.
        Item's 'id' is an integer internally used for referring to an item
        read from the database before.
        The item_values dict should not provide a value for the key 'id'
        if it does it will be ignoered.
        This function creates a new instance (= new id) of this item
        in the database.
        """
        with self.conn:
            item_values['id'] = None
            self.cursor.execute("""INSERT INTO items VALUES
                                   (:id,
                                    :name,
                                    :function,
                                    :weight,
                                    :volume,
                                    :price,
                                    :amount)""",
                                item_values)

    def get_all_items(self):
        """
        Returns a list of dictionaries of all items in the database.
        item_list is a list containg a dictionary for every item
        with the attribute's name (String) as key to the corresponding value.
        Item's 'id' can be used later when referring to an item
        read from the database using this function.
        """
        with self.conn:
            # get the raw item-data from the database
            self.cursor.execute("""SELECT * FROM items""")
            items_raw = self.cursor.fetchall()

        # reserve space in list for all items
        items = len(items_raw)*[None]

        # add a dictionary with attributes for every item to the list
        for index, item_tuple in enumerate(items_raw):
            item = {'id':       item_tuple[0],
                    'name':     item_tuple[1],
                    'function': item_tuple[2],
                    'weight':   item_tuple[3],
                    'volume':   item_tuple[4],
                    'price':    item_tuple[5],
                    'amount':   item_tuple[6]}
            items[index] = item

        return items

    def update_item(self, item_values):
        """
        This function modifies an existing instance (refered by its id)
        of items in the database with the values provided in item_values.
        item_values must be a dict with an attribute's name (string) as key
        to the corresponding value.
        Item's 'id' is an integer internally used for referring to an item
        read from the database before.
        The item_values dict must provide a value for the key 'id'
        if it does not the update will be ignoered.
        """
        with self.conn:
            self.cursor.execute("""UPDATE items SET
                                       name =  :name,
                                       function = :function,
                                       weight = :weight,
                                       volume = :volume,
                                       price = :price,
                                       amount = :amount
                                   WHERE id = :id""",
                                item_values)


if __name__ == "__main__":
    """
    TODO: Execute some tests.
    EDIT: Run: 'py.test -s' to run all the existing tests.
    Might be changed in the future.
    """
    pass
