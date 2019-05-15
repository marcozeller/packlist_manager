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
__version__ = "0.0.8"
__license__ = "MIT"

db_name = 'databases/manual_testing.db'

default_values_new_item = {'name':     "Give a Name",
                           'function': "Describe Function",
                           'weight':   "0",
                           'volume':   "0",
                           'price':    "0",
                           'amount':   "0"}

default_values_new_pack = {'name':     "Give a Name",
                           'function': "Describe Function"}

language_english = {'name':         "Name: ",
                    'function':     "Function: ",
                    'weight':       "Weight: ",
                    'volume':       "Volume: ",
                    'price':        "Price: ",
                    'amount':       "Amount: ",
                    'main_menu':    "Main Menu",
                    'add_new_item': "Add a new Item",
                    'list_items':   "List Items",
                    'edit_item':    "Edit Item",
                    'add_new_pack': "Add a new Pack",
                    'list_packs':   "List Packs",
                    'edit_pack':    "Edit Pack",
                    'select_items': "Select Items:",
                    'select_packs': "Select Packs:"}

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
        return vl['name'] + ' (id = ' + str(vl['id']) + ')'

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.selected_item = act_on_this
        if keypress == ord('d'):
            # delete the item and redraw the screen
            self.parent.parentApp.db.delete_item(act_on_this)
            self.parent.parentApp.switchForm('LIST_ITEMS')
        else:
            # go to the edit item screen
            self.parent.parentApp.switchForm('EDIT_ITEM')


class ListItems(nps.ActionFormMinimal):
    def create(self):
        item_list = self.parentApp.db.get_all_items()
        self.item_list_widget = self.add(ItemList,
                                         values=item_list,
                                         scroll_exit=True,
                                         exit_right=True)

        # Setup handler for deleting an item from list:
        # If the key 'd' is pressed call the function
        # item_list.actionHighlighted automatically with the right paramters.
        self.handlers[ord('d')] = self.item_list_widget.h_act_on_highlighted
        # TODO: remove unneeded handlers

    def beforeEditing(self):
        self.item_list_widget.values = self.parentApp.db.get_all_items()

    def on_ok(self):
        self.parentApp.setNextForm('MAIN')


class EditItem(nps.ActionFormV2):
    """
    Screen containing a formular to edit the attributes of an existing item.
    It has an 'OK' button which updates the item's value in the database and
    a 'CANCEL' button to leave the formular without changing the database.
    """
    def fill_in_fields(self):
        self._name.value = self.parentApp.selected_item['name']
        self._function.value = self.parentApp.selected_item['function']
        self._weight.value = str(self.parentApp.selected_item['weight'])
        self._volume.value = str(self.parentApp.selected_item['volume'])
        self._price.value = str(self.parentApp.selected_item['price'])
        self._amount.value = str(self.parentApp.selected_item['amount'])

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

    def beforeEditing(self):
        # fill in the fields with the default values
        self.fill_in_fields()

    def on_ok(self):
        """
        Gets called when the 'OK' button is pressed.
        Updates all the attributes in the database.
        """
        # create a dictionary containing the new attributes of the item
        item_data = {}
        item_data['id'] = self.parentApp.selected_item['id']
        item_data['name'] = self._name.value
        item_data['function'] = self._function.value
        item_data['weight'] = int(self._weight.value)
        item_data['volume'] = int(self._volume.value)
        item_data['price'] = int(self._price.value)
        item_data['amount'] = int(self._amount.value)

        # send the dictionary to the database interface
        self.parentApp.db.update_item(item_data)

        # go back to main screen
        self.parentApp.setNextForm('LIST_ITEMS')

    def on_cancel(self):
        """
        Gets called when the 'CANCEL' button is pressed.
        Make no changes to the database and exit the formular.
        """
        # go back to main screen
        self.parentApp.setNextForm('LIST_ITEMS')


class SelectItems(nps.MultiSelectAction):
    def display_value(self, vl):
        return str(vl['selected']) + 'x :' + vl['name']

    def before_editing(self):
        self.h_select()

    def actionHighlighted(self, act_on_this, keypress):
        if keypress == ord('+'):
            # increase the selected amount
            act_on_this['selected'] += 1
            # set selected if was zero before
            if act_on_this['selected'] == 1:
                self.h_select_toggle(keypress)

        elif keypress == ord('-'):
            # decrease the selected amount only if positive
            if act_on_this['selected'] > 0:
                act_on_this['selected'] -= 1
                # unselect if reches zero
                if act_on_this['selected'] == 0:
                    self.h_select_toggle(keypress)
        else:
            # TODO: open popup to select amount using slider
            pass

    def actionSelected(self, act_on_these, keypress):
        return act_on_these


class SelectPacks(nps.MultiSelectAction):
    def display_value(self, vl):
        return str(vl['selected']) + 'x :' + vl['name']

    def before_editing(self):
        self.h_select()

    def actionHighlighted(self, act_on_this, keypress):
        if keypress == ord('+'):
            # increase the selected amount
            act_on_this['selected'] += 1
            # set selected if was zero before
            if act_on_this['selected'] == 1:
                self.h_select_toggle(keypress)

        elif keypress == ord('-'):
            # decrease the selected amount only if positive
            if act_on_this['selected'] > 0:
                act_on_this['selected'] -= 1
                # unselect if reches zero
                if act_on_this['selected'] == 0:
                    self.h_select_toggle(keypress)
        else:
            # TODO: open popup to select amount using slider
            pass

    def actionSelected(self, act_on_these, keypress):
        return act_on_these


class AddPack(nps.ActionFormV2):
    """
    Screen containing a formular to enter the attributes of a new pack.
    It has an 'OK' button which saves the new pack in the database and
    a 'CANCEL' button to leave the formular without changing the database.
    """
    def reset_fields(self):
        self._name.value = default_values_new_pack['name']
        self._function.value = default_values_new_pack['function']

    def create(self):
        """
        Draws the formular with fields to enter the attributes.
        Fills the field with default values.
        Draws a list of items to choose from.
        """
        # TODO: Draws a list of packs to choose from.
        # draw the fields needed to enter the attributes
        self._name = self.add(nps.TitleText, name=language['name'])
        self._function = self.add(nps.TitleText, name=language['function'])

        self.add(nps.TitleFixedText,
                 name=language['select_items'])

        item_list = self.parentApp.db.get_all_items()
        for item in item_list:
            item['selected'] = 0
        self.item_chooser = self.add(SelectItems,
                                     values=item_list,
                                     scroll_exit=True,
                                     exit_right=True,
                                     max_height=10)

        self.add(nps.TitleFixedText,
                 name=language['select_packs'])

        pack_list = self.parentApp.db.get_all_packs()
        for pack in pack_list:
            pack['selected'] = 0
        self.pack_chooser = self.add(SelectPacks,
                                     values=pack_list,
                                     scroll_exit=True,
                                     exit_right=True,
                                     max_height=10)

        # there seems to be a bug in the library this fixes it
        self.item_chooser.vale = self.item_chooser.values
        self.pack_chooser.vale = self.pack_chooser.values

        # Setup handler for selecting and unselecting items from list:
        # If the key '+' or '-' is pressed call the function
        # item_chooser.actionHighlighted automatically with the right paramters.
        item_chooser_handlers = {ord('+'): self.item_chooser.h_act_on_highlighted,
                                 ord('-'): self.item_chooser.h_act_on_highlighted}

        self.item_chooser.add_handlers(item_chooser_handlers)

        # Setup handler for selecting and unselecting packs from list:
        # If the key '+' or '-' is pressed call the function
        # pack_chooser.actionHighlighted automatically with the right paramters.
        pack_chooser_handlers = {ord('+'): self.pack_chooser.h_act_on_highlighted,
                                 ord('-'): self.pack_chooser.h_act_on_highlighted}

        self.pack_chooser.add_handlers(pack_chooser_handlers)
        # TODO: remove unneeded handlers

        # fill in the fields with the default values
        self.reset_fields()

    def beforeEditing(self):
        self.item_chooser.values = self.parentApp.db.get_all_items()
        for item in self.item_chooser.values:
            item['selected'] = 0
        self.item_chooser.h_select_none('r')

        self.pack_chooser.values = self.parentApp.db.get_all_packs()
        for pack in self.pack_chooser.values:
            pack['selected'] = 0
        self.pack_chooser.h_select_none('r')

    def on_ok(self):
        """
        Gets called when the 'OK' button is pressed.
        Saves all the attributes into the database.
        """
        # create a dictionary containing the attributes of the new pack
        pack_data = {}
        pack_data['name'] = self._name.value
        pack_data['function'] = self._function.value

        # send the dictionary to the database interface
        included_items = self.item_chooser.h_act_on_selected('a')
        included_packs = self.pack_chooser.h_act_on_selected('a')
        self.parentApp.db.store_new_pack(pack_data, included_items, included_packs)

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


class PackList(nps.MultiLineAction):
    def display_value(self, vl):
        return vl['name'] + ' (id = ' + str(vl['id']) + ')'

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.selected_pack = act_on_this
        if keypress == ord('d'):
            # delete the item and redraw the screen
            self.parent.parentApp.db.delete_pack(act_on_this)
            self.parent.parentApp.switchForm('LIST_PACKS')
        else:
            # go to the edit item screen
            self.parent.parentApp.switchForm('EDIT_PACK')


class ListPacks(nps.ActionFormMinimal):
    def create(self):
        pack_list = self.parentApp.db.get_all_packs()
        self.pack_list_widget = self.add(PackList,
                                         values=pack_list,
                                         scroll_exit=True,
                                         exit_right=True)

        # Setup handler for deleting an item from list:
        # If the key 'd' is pressed call the function
        # item_list.actionHighlighted automatically with the right paramters.
        self.handlers[ord('d')] = self.pack_list_widget.h_act_on_highlighted
        # TODO: remove unneeded handlers

    def beforeEditing(self):
        self.pack_list_widget.values = self.parentApp.db.get_all_packs()

    def on_ok(self):
        self.parentApp.setNextForm('MAIN')


class EditPack(nps.ActionFormV2):
    """
    Screen containing a formular to edit the attributes of an existing pack.
    It has an 'OK' button which updates the pack's values in the database and
    a 'CANCEL' button to leave the formular without changing the database.
    """
    def fill_in_fields(self):
        pack = self.parentApp.selected_pack
        self._name.value = pack['name']
        self._function.value = pack['function']

        # get the calculated values for the selected_pack
        pack_values = self.parentApp.db.get_attributes_pack(pack)

        # fill in the fields accordingly
        self._weight.value = str(pack_values['weight'])
        self._volume.value = str(pack_values['volume'])
        self._price.value = str(pack_values['price'])
        self._amount.value = str(pack_values['amount'])

    def create(self):
        """
        Draws the formular with fields to enter the attributes.
        Fills the field with default values.
        """
        # draw the fields needed to enter the attributes
        self._name = self.add(nps.TitleText, name=language['name'])
        self._function = self.add(nps.TitleText, name=language['function'])
        self._weight = self.add(nps.TitleFixedText, name=language['weight'])
        self._volume = self.add(nps.TitleFixedText, name=language['volume'])
        self._price = self.add(nps.TitleFixedText, name=language['price'])
        self._amount = self.add(nps.TitleFixedText, name=language['amount'])

        self.add(nps.TitleFixedText,
                 name=language['select_items'])
        self.item_chooser = self.add(SelectItems,
                                     values=None,
                                     scroll_exit=True,
                                     exit_right=True,
                                     max_height=10)

        self.add(nps.TitleFixedText,
                 name=language['select_packs'])
        self.pack_chooser = self.add(SelectPacks,
                                     values=None,
                                     scroll_exit=True,
                                     exit_right=True,
                                     max_height=10)

        # Setup handler for selecting and unselecting items from list:
        # If the key '+' or '-' is pressed call the function
        # item_list.actionHighlighted automatically with the right paramters.
        # TODO
        self.handlers[ord('+')] = self.item_chooser.h_act_on_highlighted
        self.handlers[ord('-')] = self.item_chooser.h_act_on_highlighted
        # TODO: remove unneeded handlers!

    def beforeEditing(self):
        # fill in the fields with the default values
        self.fill_in_fields()

        top_pack = self.parentApp.selected_pack

        included_items = self.parentApp.db.get_items_in_pack(top_pack)
        not_included_items = self.parentApp.db.get_items_not_in_pack(top_pack)
        selected_items_indices = []

        for index, item in enumerate(included_items):
            # double check if really selected
            # TODO: throw an error in future
            if item['selected'] > 0:
                selected_items_indices.append(index)

        self.item_chooser.values = included_items + not_included_items
        self.item_chooser.value = selected_items_indices

        # TODO: when implemented use functions from database
        included_packs = []
        # included_packs = self.parentApp.db.get_packs_in_pack(top_pack)
        not_included_packs = []
        # not_included_packs = self.parentApp.db.get_packs_not_in_pack(top_pack)

        selected_packs_indices = []

        for index, pack in enumerate(included_packs):
            # double check if really selected
            # TODO: throw an error in future
            if pack['selected'] > 0:
                selected_packs_indices.append(index)

        self.pack_chooser.values = included_packs + not_included_packs
        self.pack_chooser.value = selected_packs_indices

        # there seems to be a bug in the library this fixes it
        self.item_chooser.vale = self.item_chooser.value
        self.pack_chooser.vale = self.pack_chooser.value

    def on_ok(self):
        """
        Gets called when the 'OK' button is pressed.
        Updates all the attributes in the database.
        """
        # create a dictionary containing the new attributes pack
        pack_data = {}
        pack_data['id'] = self.parentApp.selected_pack['id']
        pack_data['name'] = self._name.value
        pack_data['function'] = self._function.value

        # send the dictionary to the database interface
        included_items = self.item_chooser.h_act_on_selected('a')
        self.parentApp.db.update_pack(pack_data, included_items)

        # go back to main screen
        self.parentApp.setNextForm('LIST_PACKS')

    def on_cancel(self):
        """
        Gets called when the 'CANCEL' button is pressed.
        Make no changes to the database and exit the formular.
        """
        # go back to main screen
        self.parentApp.setNextForm('LIST_PACKS')


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
        self.add_item = self.addForm('EDIT_ITEM',
                                     EditItem,
                                     name=language['edit_item'])
        self.add_item = self.addForm('ADD_PACK',
                                     AddPack,
                                     name=language['add_new_pack'])
        self.add_item = self.addForm('LIST_PACKS',
                                     ListPacks,
                                     name=language['list_packs'])
        self.add_item = self.addForm('EDIT_PACK',
                                     EditPack,
                                     name=language['edit_pack'])


if __name__ == "__main__":
    """
    Runs the application and connects the user interface to the database.
    """
    app = App()
    app.db_name = db_name
    app = app.run()
