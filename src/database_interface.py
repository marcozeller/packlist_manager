#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO: Module Docstring
"""
import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_db()

    def initialize_db(self):
        """
        Creates the tables needed for storing the data if
        they do not already exist
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
        item_values is a dict with keys and values
        TODO: make this Docstring more explainatory
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
    TODO: Execute some tests
    """
    pass
