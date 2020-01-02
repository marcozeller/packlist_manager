#!/usr/bin/env Python3
import PySimpleGUI as sg

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


def get_list_items_win():
    # ------ List Items ------------- #
    list_items_layout = [
                         [sg.Listbox(values=['Listbox ' + str(i) for i in range(100)], size=(60, 10))],
                         [sg.Cancel()]
                        ]

    list_items_win = sg.Window(
                 'List Items',
                 list_items_layout,
                 resizable=True,
                 )

    return list_items_win


def get_add_pack_win():
    # ------ Add Pack --------------- #
    add_pack_layout = [
                       [sg.Text('Name:'), sg.InputText('Give a Name', key='name')],
                       [sg.Text('Function:'), sg.InputText('Describe Function', key='function')],
                       #[sg.Text('Weight [kg]:'), sg.Text('0', key='weight')],
                       #[sg.Text('Volume [L]:'), sg.Text('0', key='volume')],
                       #[sg.Text('Price [CHF]:'), sg.Text('0', key='price')],
                       #[sg.Text('Amount:'), sg.Text('0', key='amount')],
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

while True:
    menu_event, menu_values = menu_win.Read(timeout=100)

    if menu_event == 'open_db_options':
        # active_win = 'add_item'
        menu_win.Hide()
        db_options_win = get_db_options_win()

        while True:
            db_options_event, db_options_values = db_options_win.Read()
            if db_options_event == 'Save':
                # TODO: save new item
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
                # TODO: save new item
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
        list_items_win = get_list_items_win()

        while True:
            list_items_event, list_items_values = list_items_win.Read()
            if list_items_event == 'Cancel':
                list_items_win.close()
                menu_win.UnHide()
                break

    elif menu_event == 'open_add_pack':
        # active_win = 'add_pack'
        menu_win.Hide()
        add_pack_win = get_add_pack_win()

        while True:
            add_pack_event, add_pack_values = add_pack_win.Read()
            if add_pack_event == 'Save':
                # TODO: save new pack
                add_pack_win.close()
                menu_win.UnHide()
                break
            elif add_pack_event == 'Cancel':
                add_pack_win.close()
                menu_win.UnHide()
                break

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
