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
        self.initialize_db()

    def initialize_db(self):
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

    def store_new_item_in_db(self, item_values):
        """
        Stores a new item in the database.
        item_values is a dict with the attribute's name (String) as key
        to the corresponding value.
        Item's 'id' is an integer internally used for referring to an item
        read from the database before.
        If the item_values dict does not provide a value for the key 'id'
        this function creates a new instance of this item in the database.
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


if __name__ == "__main__":
    """
    TODO: Execute some tests.
    EDIT: Run: 'py.test -s' to run all the existing tests.
    Might be changed in the future.
    """
    pass
