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
                                   id integer PRIMARY KEY,
                                   name text,
                                   function text,
                                   weight integer,
                                   volume integer,
                                   price integer,
                                   amount integer) """)

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS packs(
                                   id integer PRIMARY KEY,
                                   name text,
                                   function text) """)

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS included_items(
                                   pack integer,
                                   item integer,
                                   amount integer,
                                   PRIMARY KEY (pack, item),
                                   FOREIGN KEY (pack) REFERENCES packs(id)
                                   ON DELETE CASCADE,
                                   FOREIGN KEY (item) REFERENCES items(id)
                                   ON DELETE CASCADE)
                                   """)

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS included_packs(
                                   pack integer,
                                   included_pack integer,
                                   amount integer,
                                   PRIMARY KEY (pack, included_pack),
                                   FOREIGN KEY (pack) REFERENCES packs(id)
                                   ON DELETE CASCADE,
                                   FOREIGN KEY (included_pack) REFERENCES packs(id)
                                   ON DELETE CASCADE)
                                   """)

            # activate the constraints on foreign_keys in database
            self.cursor.execute("""PRAGMA foreign_keys = ON""")

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
        The return value is a list containg a dictionary for every item
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

    def delete_item(self, item_values):
        """
        This function deletes an existing instance (refered by its id)
        of item in the database with the values provided in item_values.
        item_values must be a dict with an integer value for the key 'id'.
        Item's 'id' is an integer internally used for referring to an item
        read from the database before.
        The item_values dict must provide a value for the key 'id'
        if it does not, nothing will be deleted.
        """
        # TODO: Maybe only mark as deleted and provide an additional function
        #       to irevertible delete it.
        with self.conn:
            self.cursor.execute("""DELETE FROM items WHERE id = :id""",
                                item_values)

    def store_new_pack(self, pack_values, included_items, included_packs):
        """
        Stores a new pack in the database.
        pack_values is a dict with the attribute's name (String) as key
        to the corresponding value.
        Pack's 'id' is an integer internally used for referring to a pack
        read from the database before.
        The pack_values dict should not provide a value for the key 'id'
        if it does it will be ignoered.
        This function creates a new instance (= new id) of this pack
        in the database.
        The parameter included_items is a list of dictionaries each dictionary
        must contain a value to the key 'id' which refers to an item in the
        database and a value to the key 'selected' which is an integer > 0
        which represents how many times the item is selected in a pack.
        The parameter included_packs is a list of dictionaries each dictionary
        must contain a value to the key 'id' which refers to an item in the
        database and a value to the key 'selected' which is an integer > 0
        which represents how many times the item is selected in a pack.
        """
        with self.conn:
            pack_values['id'] = None
            self.cursor.execute("""INSERT INTO packs VALUES
                                   (:id,
                                    :name,
                                    :function)""",
                                pack_values)

            pack_values['id'] = self.cursor.lastrowid

            # catch and handle empty packs
            if included_items is None:
                included_items = []

            for item in included_items:
                if item['selected'] > 0:
                    self.cursor.execute("""INSERT INTO included_items VALUES
                                           (:pack_id,
                                            :item_id,
                                            :selected)""",
                                        {'pack_id': pack_values['id'],
                                         'item_id': item['id'],
                                         'selected': item['selected']})

            # catch and handle empty packs
            if included_packs is None:
                included_packs = []

            for pack in included_packs:
                if pack['selected'] > 0:
                    self.cursor.execute("""INSERT INTO included_packs VALUES
                                           (:pack_id,
                                            :included_pack_id,
                                            :selected)""",
                                        {'pack_id': pack_values['id'],
                                         'included_pack_id': pack['id'],
                                         'selected': pack['selected']})

    def get_all_packs(self):
        """
        Returns a list of dictionaries of all packs in the database.
        The return value is a list containg a dictionary for every pack
        with the attribute's name (String) as key to the corresponding value.
        Pack's 'id' can be used later when referring to a pack
        read from the database using this function.
        """
        with self.conn:
            # get the raw item-data from the database
            self.cursor.execute("""SELECT * FROM packs""")
            packs_raw = self.cursor.fetchall()

        # reserve space in list for all packs
        packs = len(packs_raw)*[None]

        # add a dictionary with attributes for every pack to the list
        for index, pack_tuple in enumerate(packs_raw):
            item = {'id':       pack_tuple[0],
                    'name':     pack_tuple[1],
                    'function': pack_tuple[2]}
            packs[index] = item

        return packs

    def delete_pack(self, pack_values):
        """
        This function deletes an existing instance (refered by its id)
        of pack in the database with the values provided in pack_values.
        pack_values must be a dict with an integer value for the key 'id'.
        Pack's 'id' is an integer internally used for referring to a pack
        read from the database before.
        The pack dict must provide a value for the key 'id'
        if it does not, nothing will be deleted.
        """
        # TODO: Maybe only mark as deleted and provide an additional function
        #       to irevertible delete it.
        with self.conn:
            self.cursor.execute("""DELETE FROM packs WHERE id = :id""",
                                pack_values)
            self.cursor.execute("""DELETE FROM included_items WHERE
                                   pack = :id""",
                                pack_values)

    def get_attributes_pack(self, pack):
        """
        Returns a dictionary with all attributes of a pack from the database.
        The parameter pack is a dictionary with an integer value for the key
        'id' representing it's internal reference for the database.
        The return value is a dictionary with the attribute's name (String) as
        key to the corresponding value.
        In case pack had stored some values for other keys than 'id' these will
        be overwritten with the values from the database.
        The values for 'weight', 'volume', 'price', and 'amount' are calculated
        recursively from the included items and packs.
        The value for 'amount' stands for how many packs of these type can be
        built with the available amounts of items.
        """
        # create a dictionary with the known return values
        pack_values = {'id':       pack['id'],
                       'name':     None,
                       'function': None,
                       'weight':   0,
                       'volume':   0,
                       'price':    0,
                       'amount':   "infinitely"}
        # if amount is not changed later this means there is neither an item
        # nor a pack included in this pack therefore in theory we can build
        # infinitely many packs of this type

        with self.conn:
            # get the raw data for all included items from the database
            self.cursor.execute("""SELECT * FROM items
                                   INNER JOIN included_items
                                   ON items.id = included_items.item
                                   AND included_items.pack = :id""",
                                pack)
            included_items_raw = self.cursor.fetchall()

        # go through all items and update pack_values accordingly
        for index, included_item in enumerate(included_items_raw):
            # read out the needed values from the raw data tuple
            name = included_item[1]
            function = included_item[2]
            weight = included_item[3]
            volume = included_item[4]
            price = included_item[5]
            amount_available = included_item[6]
            amount_selected = included_item[9]

            # update values according to item's attribute and amount selected
            pack_values['name'] = name
            pack_values['function'] = function
            pack_values['weight'] += amount_selected * weight
            pack_values['price'] += amount_selected * price
            pack_values['volume'] += amount_selected * volume
            amount = amount_available // amount_selected

            if index == 0:
                pack_values['amount'] = amount
            else:
                pack_values['amount'] = min(amount,
                                            pack_values['amount'])

        return pack_values

    def get_items_in_pack(self, pack):
        """
        Returns a list of dictionaries, containing the attributes of all the
        items included in the by the argument specified pack.
        The parameter pack is a dictionary with an integer value for the key
        'id' representing it's internal reference for the database.
        The dictionaries have in addtion to the standard values a value to the
        key 'selected' which is an integer > 0 which represents how many times
        the item is selected in a pack.
        """
        with self.conn:
            # get the raw data for all included items from the database
            self.cursor.execute("""SELECT * FROM items
                                   INNER JOIN included_items
                                   ON items.id = included_items.item
                                   WHERE
                                   included_items.pack = :id""",
                                pack)
            included_items_raw = self.cursor.fetchall()

        # reserve space in list for all items
        included_items = len(included_items_raw)*[None]

        # add a dictionary with attributes for every item to the list
        for index, item_tuple in enumerate(included_items_raw):
            item = {'id':       item_tuple[0],
                    'name':     item_tuple[1],
                    'function': item_tuple[2],
                    'weight':   item_tuple[3],
                    'volume':   item_tuple[4],
                    'price':    item_tuple[5],
                    'amount':   item_tuple[6],
                    'selected': item_tuple[9]}
            included_items[index] = item

        return included_items

    def get_items_not_in_pack(self, pack):
        """
        Returns a list of dictionaries, containing the attributes of all the
        items not included in the by the argument specified pack.
        The parameter pack is a dictionary with an integer value for the key
        'id' representing it's internal reference for the database.
        For convenience the returned dictionaries have a value to the key
        'selected' which is initialised with 0.
        """
        with self.conn:
            # get the raw data for all not included items from the database
            self.cursor.execute("""SELECT DISTINCT id, name, function, weight,
                                       volume, price, items.amount
                                   FROM items
                                   LEFT JOIN included_items
                                   ON items.id = included_items.item
                                   EXCEPT
                                   SELECT DISTINCT id, name, function, weight,
                                       volume, price, items.amount
                                   FROM items
                                   LEFT JOIN included_items
                                   ON items.id = included_items.item
                                   WHERE included_items.pack = :id""",
                                pack)
            not_included_items_raw = self.cursor.fetchall()

        # reserve space in list for all items
        not_included_items = len(not_included_items_raw)*[None]

        # add a dictionary with attributes for every item to the list
        for index, item_tuple in enumerate(not_included_items_raw):
            item = {'id':              item_tuple[0],
                    'name':            item_tuple[1],
                    'function':        item_tuple[2],
                    'weight':          item_tuple[3],
                    'volume':          item_tuple[4],
                    'price':           item_tuple[5],
                    'amount':          item_tuple[6],
                    'selected': 0}
            not_included_items[index] = item

        return not_included_items

    def update_pack(self, pack_values, included_items):
        """
        This function modifies an existing instance (specified by it's id in
        pack_attributes) of pack_attributes in the database with the values
        provided in pack and item_amounts.
        The parameter pack_attributes must be a dict with an attribute's name
        (string) as key to 'id', 'name', and 'function' - all other values are
        ignored.
        The paramter included_items must be a list of dictionaries of items to
        to include in the pack.
        Each dictionary must have a value for key 'id' and 'selected' all other
        values are ignored.
        Where the value for 'id' is an integer internally used for referring
        to the including item.
        The value to the key 'selected' is an integer > 0 which represents how
        many times the item is selected in a pack.
        """
        with self.conn:
            self.cursor.execute("""UPDATE packs SET
                                       name =  :name,
                                       function = :function
                                   WHERE id = :id""",
                                pack_values)

            self.cursor.execute("""DELETE FROM included_items WHERE
                                   pack = :id""",
                                pack_values)

            # catch and handle empty packs
            if included_items is None:
                included_items = []

            for item in included_items:
                if item['selected'] > 0:
                    self.cursor.execute("""INSERT INTO included_items VALUES
                                           (:pack_id,
                                            :item_id,
                                            :selected)""",
                                        {'pack_id': pack_values['id'],
                                         'item_id': item['id'],
                                         'selected': item['selected']})

    def get_packs_in_pack(self, pack):
        """
        Returns a list of dictionaries, containing the attributes of all the
        packs included in the by the argument specified pack.
        The parameter pack is a dictionary with an integer value for the key
        'id' representing it's internal reference for the database.
        The dictionaries have in addtion to the standard values a value to the
        key 'selected' which is an integer > 0 which represents how many times
        the pack is selected in a pack.
        """
        with self.conn:
            # get the raw data for all included packs from the database
            self.cursor.execute("""SELECT * FROM packs
                                   INNER JOIN included_packs
                                   ON packs.id = included_packs.included_pack
                                   WHERE
                                   included_packs.pack = :id""",
                                pack)
            included_packs_raw = self.cursor.fetchall()

        # reserve space in list for all packs
        included_packs = len(included_packs_raw)*[None]

        # add a dictionary with attributes for every pack to the list
        for index, pack_tuple in enumerate(included_packs_raw):
            pack = {'id':       pack_tuple[0],
                    'name':     pack_tuple[1],
                    'function': pack_tuple[2],
                    'selected': pack_tuple[5]}
            included_packs[index] = pack

        return included_packs

    def leads_to_circular_reference(self, pack, pack_to_include):
        """
        Returns True if pack_to_include or any of it's sub-packs contains pack.
        If and only if this function returns False it is save to
        include pack_to_include into pack, without breaking the program later.
        """
        if pack['id'] == pack_to_include['id']:
            return True
        else:
            included_packs = self.get_packs_in_pack(pack_to_include)
            for sub_pack in included_packs:
                if self.leads_to_circular_reference(pack, sub_pack):
                    return True
            return False

    def get_packs_not_in_pack(self, pack):
        """
        Returns a list of dictionaries, containing the attributes of all the
        packs not included in the by the argument specified pack.
        The parameter pack is a dictionary with an integer value for the key
        'id' representing it's internal reference for the database.
        For convenience the returned dictionaries have a value to the key
        'selected' which is initialised with 0.
        """
        with self.conn:
            # get the raw data for all not included packs from the database
            self.cursor.execute("""SELECT DISTINCT id, name, function
                                   FROM packs
                                   LEFT JOIN included_packs
                                   ON packs.id = included_packs.included_pack
                                   EXCEPT
                                   SELECT DISTINCT id, name, function
                                   FROM packs
                                   LEFT JOIN included_packs
                                   ON packs.id = included_packs.included_pack
                                   WHERE included_packs.pack = :id""",
                                pack)
            not_included_packs_raw = self.cursor.fetchall()
            not_included_packs = []

        # add a dictionary with attributes for every pack to the list
        for index, pack_tuple in enumerate(not_included_packs_raw):
            pack_to_select = {'id':              pack_tuple[0],
                              'name':            pack_tuple[1],
                              'function':        pack_tuple[2],
                              'selected': 0}
            if not self.leads_to_circular_reference(pack, pack_to_select):
                not_included_packs.append(pack_to_select)

        return not_included_packs


if __name__ == "__main__":
    """
    TODO: Execute some tests.
    EDIT: Run: 'py.test -s' to run all the existing tests.
    Might be changed in the future.
    """
    pass
