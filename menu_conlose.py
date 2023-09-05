from settings import version, lp_store_parser_number_view_items, sort_list, sales_tax, filter_lp_number, save_settings, \
    settings, items_component_settings, change_lp_store, items_in_lp_store
from items_faction_wars import items_faction_wars_state_protectorate, items_component
from lp_store_items_state_protectorate import items_component_state_protectorate
from save_load import save_json, load_json
from colors import color_lp_profit

import sys


#items = items_faction_wars_state_protectorate + items_component


def menu_greetings():
    print(f"LP Store Calculator - Version: {version}")
    print(f'Items All Count: {len(items_component_settings)}')
    print(f'Items Components Count: {len(items_component)}  !!! Change to Actual LP Store')
    print(f'Items Market Count: {len(items_faction_wars_state_protectorate)} !!! Change to Actual LP Store')
    print(f'\n!!! CAUTION !!!')
    print('Please be considerate, and check prices. \nSome missiles are not counting correctly at the moment.', end='')
    # print('',end='')
    print()


def menu_console_interface():
    print('\n1. Show old Prices'
          f'\n2. Update Prices (≈ {len(items_component_settings) // 3} sec).'
          '\n3. Settings'
          '\n9. About'
          '\n0. Exit')

    try:
        ask = int(input('\nSelect menu: '))
    except:
        print('Please, enter number')
        ask = None
        menu_console_interface()

    if ask == 1:
        # Отображение цен из файла lp_state_protectorate.json
        load_json()
        menu_console_interface()
    elif ask == 2:
        # Запуск скрипта
#        save_json()
        print(f'\nStart Downloading Prices. (≈ {len(items_component_settings) // 3} sec)')
    elif ask == 3:
        # Settings Menu
        settings_menu()
        menu_console_interface()
    elif ask == 9:
        # About page
        print('\nLP Calculator - This script is designed to get actual prices when cashing out LP (Loyalty Points). '
              '\nAt the moment the script works with LP State Protectorate. And with the marketplace in Jita.'
              '\nWith questions and suggestions, you can write to the in-game mail.'
              '\nDeveloper: Allehandro')
        menu_console_interface()
    elif ask == 0:
        print("\nThank's for using this script. Fly Save!!!")
        sys.exit()
    else:
        menu_console_interface()


def settings_menu():
    # Функция для отображения, и изменения настроек скрипта
    print('\nSettings:')
    print(f'1. Number of elements to be displayed: {settings["lp_store_parser_number_view_items"]}'
          f'\n2. Sorting (Sell / Buy): {settings["sort_list"]}'
#          f'\n3. Filter by counter of positions: {settings["sort_list_counter_2_view"]}'
          f'\n4. Filter by min isk value: {settings["filter_min_isk_per_lp"]}'
          f"\n5. Sale Tax change (Don't work): {sales_tax} %"
          f"\n6. LP Store: ({settings['lp_faction']})"
          f'\n0. Save and Back')

    ask = int(input('\nSelect menu: '))

    if ask == 1:
        print(f'\nNumber of elements to be displayed: {settings["lp_store_parser_number_view_items"]}'
              f'\n1. Change to: All'
              f'\n2. Change to other value: '
              f'\n0. Back')
        ask_2 = int(input(f'\nPlease enter digit: '))
        if ask_2 == 1:
            print('\nNumber of elements to be displayed change to: all')
            settings["lp_store_parser_number_view_items"] = 'all'
            save_settings(settings)
#            menu_console_interface()
        elif ask_2 == 2:
            try:
                settings["lp_store_parser_number_view_items"] = int(input("\nSpecify a value for how many items to show when sorting: "))
                save_settings(settings)
#                menu_console_interface()
            except:
                print("\nPlease enter digits")
                settings["lp_store_parser_number_view_items"] = int(input("Specify a value for how many items to show when sorting: "))
                save_settings(settings)
#                menu_console_interface()
        else:
            settings_menu()

    elif ask == 2:
        print(f'\nSorting: {settings["sort_list"]}'
              f'\n1. Sorting change to: Sell'
              f'\n2. Sorting change to: Buy '
              f'\n0. Back')
        ask_2 = int(input('\nSelect sorting: '))
        if ask_2 == 1:
            print('Sorting change to Sell')
            settings["sort_list"] = "sell_lp_profit"
            save_settings(settings)
            menu_console_interface()
        elif ask_2 == 2:
            print('Sorting change to Buy:')
            settings["sort_list"] = "buy_lp_profit"
            save_settings(settings)
            menu_console_interface()

#    elif ask == 3:
#        print(f'\nFilter by number of LPs on isk: {[settings["sort_list_counter_2_view"]]}')
#        ask_2 = int(input('1. Change value'
#                          '\n0. Back'
#                          '\nEnter digit: '))
#        if ask_2 == 1:
#            settings["sort_list_counter_2_view"] = int(input('Enter value of minimum isk per 1 LP: '))
#            print(f'\nChange Filter by number of LPs on isk to: {[settings["sort_list_counter_2_view"]]}')
#            save_settings(settings)
#            menu_console_interface()
#        else:
#            settings_menu()

    elif ask == 4:
        print(f'\nFilter by min isk value: {settings["filter_min_isk_per_lp"]}')
        ask_2 = int(input('1. Change value'
                          '\n0. Back'
                          '\nEnter digit: '))
        if ask_2 == 1:
            try:
                settings["filter_min_isk_per_lp"] = int(input('\nEnter minimum isk per LP: '))
                print(f'\nChange Filter by min isk value: {settings["filter_min_isk_per_lp"]}')
                save_settings(settings)
            except:
                print('Please, enter digits: ')
                settings["filter_min_isk_per_lp"] = int(input('Enter minimum isk per LP: '))
                settings_menu()
        else:
            settings_menu()

    elif ask == 5:
        print(f"\nSale Tax (Don't work): {settings['sales_tax'] * 100} %")
        ask_2 = int(input('1. Change value'
                          '\n0. Back'
                          '\nEnter digit: '))
        if ask_2 == 1:
            try:
                settings['sales_tax'] = int(input('Change to %: '))
                settings['sales_tax'] = settings['sales_tax'] / 100
                print(f'\nSales Tax Change to: {settings["sales_tax"] * 100} %')
                save_settings(settings)
                menu_console_interface()
            except:
                print('Please, enter digits.')
                settings['sales_tax'] = int(input('Change to %: '))
                settings['sales_tax'] = settings['sales_tax'] / 100
                settings_menu()
        elif ask_2 == 0:
            settings_menu()
        else:
            settings_menu()
    elif ask == 6:
        print(f'\nChange LP Store. Now: {settings["lp_faction"]}')
        ask_lp_store = int(input('1. State Protectorate (Caldari Navy)'
#                          '\n2. Federal Defence Union (Gallente)'
#                          '\n3. 24th Imperial Crusade (Amarr)'
#                          '\n4. Tribal Liberation Force (Minmatar)'
                          '\n5. Sisters Of Eve'
#                          '\n6. Outer Ring Excavations - ORE'
                          '\n0. Back'
                          '\nEnter digit: '))
        if ask_lp_store == 1:
            settings["lp_faction"] = "state_protectorate"
            print(f'\nLP Store Change to: {settings["lp_faction"]}')
            change_lp_store(ask_lp_store)
#            save_settings(settings)
#            items_component_settings = items_component_state_protectorate + items_faction_wars_state_protectorate
#            items_in_lp_store = items_faction_wars_state_protectorate
            return items_component_settings, items_in_lp_store, settings
        elif ask_lp_store == 5:
#            lp_faction = "sisters_of_eve"
            settings["lp_faction"] = "sisters_of_eve"
            change_lp_store(ask_lp_store)
            print(f'\nLP Store Change to: {settings["lp_faction"]}')
            save_settings(settings)
#            return settings["lp_faction"]
        else:
            settings_menu()
        return items_component_settings, items_in_lp_store, settings


    elif ask == 0:
        save_settings(settings)
        menu_console_interface()
    else:
        settings_menu()

    return sort_list, sales_tax, filter_lp_number, settings
