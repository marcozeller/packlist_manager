#!/usr/bin/env Python3
import PySimpleGUI as sg
import database_interface as dbi
import metadata.languages_default_values as met
import decimal

__author__ = "Marco Zeller"
__version__ = "0.0.10"
__license__ = "MIT"

db_path = 'databases/manual_gui_testing.db'

default_values_new_item = met.default_values_new_item
default_values_new_pack = met.default_values_new_pack
unit_for = met.unit_for
language = met.language_english

sg.ChangeLookAndFeel('SystemDefault')
# print(sg.Window('Packlist Manager: Add New Item').Layout(add_item_layout).Read())


def get_menu_win():
    # ------ Menu ------------------- #
    menu_layout = [
                   [sg.Button('Database Options', key='open_db_options')],
                   [sg.Button('Add Item', key='open_add_item')],
                   [sg.Button('List Items', key='open_list_items')],
                   [sg.Button('Add Pack', key='open_add_pack')],
                   [sg.Button('List Packs', key='open_list_packs')],
                  ]

    menu_win = sg.Window(
                 'Main Menu',
                 menu_layout,
                 resizable=True,
                 )

    return menu_win


def get_db_options_win():
    # ------ Change DB -------------- #
    db_options_layout = [
                 [sg.Text('Choose A Folder', size=(35, 1))],
                 [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
                     sg.InputText('Default Folder'), sg.FolderBrowse()],
                 [sg.Save(tooltip='Click to submit this window'), sg.Cancel()]
               ]

    db_options_win = sg.Window(
                 'Add New Item',
                 db_options_layout,
                 resizable=True,
                 )

    return db_options_win


def get_add_item_win():
    # ------ Add Item --------------- #
    add_item_layout = [
                       [sg.Text('Name:'), sg.InputText('Give a Name', key='name', tooltip='Give your Item a nice name')],
                       [sg.Text('Function:'), sg.InputText('Describe Function', key='function')],
                       [sg.Text('Weight [kg]:'), sg.InputText('0', key='weight')],
                       [sg.Text('Volume [L]:'), sg.InputText('0', key='volume')],
                       [sg.Text('Price [CHF]:'), sg.InputText('0', key='price')],
                       [sg.Text('Amount:'), sg.InputText('0', key='amount')],
                       [sg.Save(), sg.Cancel()],
                      ]

    add_item_win = sg.Window(
                 'Add New Item',
                 add_item_layout,
                 resizable=True,
                 )

    return add_item_win


class DisplayItem:
    def __init__(self, item_dict):
        self.item_dict = item_dict

    def __str__(self):
        return '(id = ' + str(self.item_dict['id']) + ') : ' + self.item_dict['name']

    def get_id(self):
        return self.item_dict['id']


def get_list_items_win(items_list):
    # ------ List Items ------------- #
    list_items_layout = [
                         [sg.Listbox(values=[DisplayItem(i) for i in items_list],
                                     size=(60, 10),
                                     bind_return_key=True,
                                     enable_events=True,
                                     select_mode=sg.LISTBOX_SELECT_MODE_BROWSE,
                                     )],
                         [sg.Button('Modify', key='modify_item'), sg.Cancel()]
                        ]

    list_items_win = sg.Window(
                 'List Items',
                 list_items_layout,
                 resizable=True,
                 )

    return list_items_win


def get_modify_item_win(item_dict):
    # ------ Modify Item --------------- #
    modify_item_layout = [
                       [sg.Text('Name:'), sg.InputText(item_dict['name'], key='name')],
                       [sg.Text('Function:'), sg.InputText(item_dict['function'], key='function')],
                       [sg.Text('Weight [kg]:'), sg.InputText(item_dict['weight'], key='weight')],
                       [sg.Text('Volume [L]:'), sg.InputText(item_dict['volume'], key='volume')],
                       [sg.Text('Price [CHF]:'), sg.InputText(item_dict['price'], key='price')],
                       [sg.Text('Amount:'), sg.InputText(item_dict['amount'], key='amount')],
                       [sg.Save(), sg.Cancel()],
                      ]

    add_item_win = sg.Window(
                 'Modify Item',
                 modify_item_layout,
                 resizable=True,
                 )

    return add_item_win


class DisplayItemToSelect:
    def __init__(self, item_dict, selected):
        self.item_dict = item_dict
        self.item_dict['selected'] = selected

    def __str__(self):
        return str(self.item_dict['selected']) + ' x ' + \
               '(id = ' + str(self.item_dict['id']) + ') : ' + \
               self.item_dict['name']

    def get_selected(self):
        return self.item_dict['selected']

    def select_more(self):
        self.item_dict['selected'] += 1

    def select_less(self):
        if self.item_dict['selected'] > 0:
            self.item_dict['selected'] -= 1

    def get_id(self):
        return self.item_dict['id']


def get_add_pack_win(items_to_display, packs_to_display):
    # ------ Add Pack --------------- #
    add_pack_layout = [
                       [sg.Text('Name:'), sg.InputText('Give a Name', key='name')],
                       [sg.Text('Function:'), sg.InputText('Describe Function', key='function')],
                       #[sg.Text('Weight [kg]:'), sg.Text('0', key='weight')],
                       #[sg.Text('Volume [L]:'), sg.Text('0', key='volume')],
                       #[sg.Text('Price [CHF]:'), sg.Text('0', key='price')],
                       #[sg.Text('Amount:'), sg.Text('0', key='amount')],
                       [sg.Button('Select Items', key='select_items'), sg.Button('Deselect Items', key='diselect_items'),],
                       [sg.Listbox(values=items_to_display,
                                   size=(60, 10),
                                   bind_return_key=False,
                                   enable_events=True,
                                   select_mode=sg.LISTBOX_SELECT_MODE_BROWSE,
                                   key='item_toggeled',
                                   )],
                       [sg.Button('Select Packs', key='select_packs'), sg.Button('Deselect Packs', key='diselect_packs'),],
                       [sg.Listbox(values=packs_to_display,
                                   size=(60, 10),
                                   bind_return_key=True,
                                   enable_events=True,
                                   key='pack_toggeled',
                                   )],
                       [sg.Save(), sg.Cancel()],
                      ]

    add_pack_win = sg.Window(
                 'Add New Pack',
                 add_pack_layout,
                 resizable=True,
                 )

    return add_pack_win


def get_list_packs_win():
    # ------ List Packs ------------- #
    list_packs_layout = [
                         [sg.Listbox(values=['Listbox ' + str(i) for i in range(100)], size=(60, 10))],
                         [sg.Cancel()]
                        ]

    list_packs_win = sg.Window(
                 'List Packs',
                 list_packs_layout,
                 resizable=True,
                 )

    return list_packs_win


# ------ Logic ------------------ #
menu_win = get_menu_win()
db = dbi.Database(db_path)

while True:
    menu_event, menu_values = menu_win.Read(timeout=100)

    if menu_event == 'open_db_options':
        # active_win = 'add_item'
        menu_win.Hide()
        db_options_win = get_db_options_win()

        while True:
            db_options_event, db_options_values = db_options_win.Read()
            if db_options_event == 'Save':
                db_options_win.close()
                menu_win.UnHide()
                break
            elif db_options_event == 'Cancel':
                db_options_win.close()
                menu_win.UnHide()
                break

    elif menu_event == 'open_add_item':
        # active_win = 'add_item'
        menu_win.Hide()
        add_item_win = get_add_item_win()

        while True:
            add_item_event, add_item_values = add_item_win.Read()
            if add_item_event == 'Save':
                add_item_values['weight'] = decimal.Decimal(add_item_values['weight'])
                add_item_values['volume'] = decimal.Decimal(add_item_values['volume'])
                add_item_values['price'] = decimal.Decimal(add_item_values['price'])
                add_item_values['amount'] = int(add_item_values['amount'])
                db.store_new_item(add_item_values)
                add_item_win.close()
                menu_win.UnHide()
                break
            elif add_item_event == 'Cancel':
                add_item_win.close()
                menu_win.UnHide()
                break

    elif menu_event == 'open_list_items':
        # active_win = 'list_items'
        menu_win.Hide()
        items_list = db.get_all_items()
        list_items_win = get_list_items_win(items_list)

        while True:
            list_items_event, list_items_values = list_items_win.Read()

            if list_items_event == 'modify_item':
                item_to_modify = list_items_values[0][0].item_dict
                list_items_win.hide()
                modify_item_win = get_modify_item_win(item_to_modify)

                while True:
                    modify_item_event, modify_item_values = modify_item_win.Read()

                    if modify_item_event == 'Save':
                        modify_item_values['id'] = item_to_modify['id']
                        modify_item_values['weight'] = decimal.Decimal(modify_item_values['weight'])
                        modify_item_values['volume'] = decimal.Decimal(modify_item_values['volume'])
                        modify_item_values['price'] = decimal.Decimal(modify_item_values['price'])
                        modify_item_values['amount'] = int(modify_item_values['amount'])
                        db.update_item(modify_item_values)

                        item_list = db.get_all_items()
                        list_items_win.close()
                        list_items_win = get_list_items_win(item_list)
                        modify_item_win.close()
                        break

                    elif modify_item_event == 'Cancel':
                        modify_item_win.close()
                        list_items_win.UnHide()
                        break

            elif list_items_event == 'Cancel':
                list_items_win.close()
                menu_win.UnHide()
                break

    elif menu_event == 'open_add_pack':
        # active_win = 'add_pack'
        menu_win.Hide()
        items_list = db.get_all_items()
        items_to_display = [DisplayItemToSelect(i, 0) for i in items_list]
        packs_list = db.get_all_packs()
        packs_to_display = [DisplayItemToSelect(i, 0) for i in packs_list]
        add_pack_win = get_add_pack_win(items_to_display, packs_to_display)

        adding_items = True
        adding_packs = True
        while True:
            add_pack_event, add_pack_values = add_pack_win.Read()
            print(add_pack_event)

            if add_pack_event == 'Save':
                included_items = [{'id': i.get_id(), 'selected': i.get_selected()} for i in items_to_display]
                included_packs = [{'id': p.get_id(), 'selected': p.get_selected()} for p in packs_to_display]

                db.store_new_pack(add_pack_values, included_items, included_packs)
                # TODO: save new pack
                add_pack_win.close()
                menu_win.UnHide()
                break
            elif add_pack_event == 'Cancel':
                add_pack_win.close()
                menu_win.UnHide()
                break
            elif add_pack_event == 'select_items':
                adding_items = True
            elif add_pack_event == 'diselect_items':
                adding_items = False
            elif add_pack_event == 'item_toggeled':
                if adding_items:
                    add_pack_values['item_toggeled'][0].select_more()
                else:
                    add_pack_values['item_toggeled'][0].select_less()
                add_pack_win.close()
                add_pack_win = get_add_pack_win(items_to_display, packs_to_display)
            elif add_pack_event == 'select_packs':
                adding_packs = True
            elif add_pack_event == 'diselect_packs':
                adding_packs = False
            elif add_pack_event == 'pack_toggeled':
                if adding_packs:
                    add_pack_values['pack_toggeled'][0].select_more()
                else:
                    add_pack_values['pack_toggeled'][0].select_less()
                add_pack_win.close()
                add_pack_win = get_add_pack_win(items_to_display, packs_to_display)

    elif menu_event == 'open_list_packs':
        # active_win = 'list_packs'
        menu_win.Hide()
        list_packs_win = get_list_packs_win()

        while True:
            list_packs_event, list_packs_values = list_packs_win.Read()
            if list_packs_event == 'Cancel':
                list_packs_win.close()
                menu_win.UnHide()
                break

    elif menu_event is None:
        menu_win.close()
