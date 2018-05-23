# uncompyle6 version 3.1.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (v3.6.5:f59c0932b4, Mar 28 2018, 17:00:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Modulate.py
import API_Calls as API, Init

def modulate(items, start_position, module_position):
    title_index = int(start_position)
    module_name = items[title_index]['title']
    module = API.createModule(module_name, module_position)
    API.publishModule(module['id'])
    print(('Created New Module - ({})').format(module_name))
    new_position = 1
    for item in items[title_index + 1:]:
        if (item['type'] == 'SubHeader') & (item['indent'] == 0):
            break
        else:
            indent = item['indent']
            if indent != 0:
                indent = indent - 1
            API.moveModuleItem(item['module_id'], item['id'], module['id'], indent, new_position)
            new_position += 1
            print(('Moved Module Item - ({})').format(item['title']))


def MasterModulateBysub(parent_module):
    print(('{} is now being modulated by subHeader positions').format(parent_module['name']))
    module_position_variable = int(parent_module['position']) + 1
    parent_module_items = API.getModuleItems(parent_module['id'])
    if parent_module_items == []:
        print('No items were found in the specified module - Process terminated')
        return
    for item in parent_module_items:
        if (item['type'] == 'SubHeader') & (item['indent'] == 0):
            modulate(parent_module_items, parent_module_items.index(item), module_position_variable)
            module_position_variable += 1

    API.deleteModule(parent_module['id'])


def MasterModulateIndiscriminate(parent_module):
    print(('{} is now being modulated indiscriminately').format(parent_module['name']))
    module_items = API.getModuleItems(parent_module['id'])
    for module_item in module_items:
        new_module = API.createModule(module_item['title'], module_item['position'])
        API.moveModuleItem(parent_module['id'], module_item['id'], new_module['id'], 0, 1)
        API.publishModule(new_module['id'])
        print(('({}) now sits in is own module').format(module_item['title']))

    API.deleteModule(parent_module['id'])
    print(('Deleted Parent Module: ({})').format(parent_module['name']))


def MasterModulate():
    print('****Module Breakup --Optional****')
    modules = API.getAllModules()
    if modules == []:
        print('This course does not contain any modules. The function will now exit.')
        print('\n')
        return
    while True:
        parent_module_name = input("If you would like to break up a module, enter its name here. To continue without breaking up any modules, enter 'NONE':")
        if parent_module_name.upper() == 'NONE':
            print('You chose not to break up any modules by entering NONE.')
            print('\n')
            return
        found = False
        for module in modules:
            if module['name'] == parent_module_name:
                parent_module = module
                found = True
                break

        if not found:
            print("A module with the specified name could not be found. Please try again. If the issue persists, enter 'NONE' to skip the function.")
        else:
            break

    while True:
        modulate_type = input("How would you like to break up the module? (Select 1, 2, or 3):\n1. Create a new Module for each item (indiscriminate)\n2. Create a module for each 0-indent subHeader found\n3. Nevermind, I don't want to break up the module\n")
        if modulate_type in ('1', '2', '3'):
            break
        else:
            print(('ERROR - {} is an invalid input. Try again.').format(modulate_type))

    if modulate_type == '1':
        MasterModulateIndiscriminate(parent_module)
    else:
        if modulate_type == '2':
            MasterModulateBysub(parent_module)
    print('\n')