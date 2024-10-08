# pyinstaller -F --icon=icon.ico main_lp_store_parser.py

# Idea:
# Отображение иконок. Можно добавить информацию об отображаемой иконке в цикл файла. С переменную, возле названия.

import requests
import time
import datetime
import sys

#from items_faction_wars import items_faction_wars_state_protectorate, items_component

from colors import color_lp_profit
from settings import DEBUG_MODE, settings, sort_list, sort_list_counter_2_view, auto_time_update, market_region, \
    regions, stations, sales_tax, version, lp_store_parser_number_view_items, load_settings, items_component_settings, \
    items_in_lp_store
from menu_conlose import menu_greetings, menu_console_interface
from save_load import save_json


start_time = time.time()
load_settings()


#items = items_faction_wars_state_protectorate + items_component
items = items_component_settings
items_prices_parsed = []
items_quantity = []
items_2_table = []
items_2_table_last_request = []
#total_price = 0

change_buy_lp_profit = None
change_sell_lp_profit = None
change_buy_volume = None


menu_greetings()
menu_console_interface()


def get_item_prices(item_id, item_name, region_id, region_name, station_id, station_name, sales_tax):
    url = "https://esi.evetech.net/latest/markets/{}/orders/?datasource=tranquility&order_type=all&page=1&type_id={}"

    headers = {'User-Agent': 'LP-Calculator'}
    prices = {}

    region_url = url.format(region_id, item_id)
    response = requests.get(region_url, headers=headers)

    if response.status_code == 200:
        orders = response.json()

        # Оставить только buy ордеры с максимальной ценой
        filtered_orders = [order for order in orders if order["location_id"] == station_id and order["is_buy_order"] and order["price"] == max([o["price"] for o in orders if o["location_id"] == station_id and o["is_buy_order"]])]

        # Оставить только sell ордеры
        sell_orders = [order for order in orders if order["location_id"] == station_id and not order["is_buy_order"]]

        min_sell_price = min(order["price"] for order in sell_orders) if sell_orders else None
        max_buy_price = max(order["price"] for order in filtered_orders) if filtered_orders else None

        trade_volume = sum(order["volume_remain"] for order in filtered_orders)

        if filtered_orders:
            buy_price = filtered_orders[0]["price"]
            profit_sell = buy_price - max_buy_price if max_buy_price is not None else None
            profit_sell_percentage = (profit_sell / buy_price) * 100 if profit_sell is not None else None

            prices[station_id] = {
                "region_name": region_name,
                "station_name": station_name,
                "item_name": item_name,
                "min_sell_price": min_sell_price,
                "max_buy_price": max_buy_price,
                "trade_volume": trade_volume,
                "best_buy_volume": filtered_orders[0]["volume_remain"] if filtered_orders else None,
                "profit_sell": profit_sell,
                "profit_sell_percentage": profit_sell_percentage
            }
    else:
        print(f"Ошибка при получении цен на товар '{item_name}' в регионе '{region_name}': {response.status_code}")

    return prices


#print(stations[0]['id'])


def items_prices():
    # Парсим цены по разным товарам
    global items_prices_parsed
#    global total_parsed_counter

    percentage_complete = 0
    cnt = 0

    for item in items:
        item_id = item["id"]
        item_name = item["item_name"]

        for region in regions:
            region_id = region["id"]
            region_name = region["name"]

            for station in stations:
                station_id = station["id"]
                station_name = station["name"]

                item_prices = get_item_prices(item_id, item_name, region_id, region_name, station_id, station_name, sales_tax)

                if item_prices and station_id in item_prices:
                    for station_id, station_prices in item_prices.items():
                        if station_prices:
                            cnt += 1
                            percentage_complete = ((cnt / len(items)) * 100)  # Прогресс в % для интерфейса
                            if DEBUG_MODE:
                                print(f"\nТовар: '{item_name}' в регионе '{region_name}' на станции '{station_name}':")

                            min_sell_price = station_prices["min_sell_price"]
                            max_buy_price = station_prices["max_buy_price"]
                            trade_volume = station_prices["trade_volume"]
                            buy_volume = station_prices["best_buy_volume"]
                            profit_sell = station_prices["profit_sell"]
                            profit_sell_percentage = station_prices["profit_sell_percentage"]

                            if DEBUG_MODE:
                                try:
                                    print(f"Sell Price: {min_sell_price:,.0f}, Buy Price: {max_buy_price:,.0f}")
                                    print(f"Торговый объем - {trade_volume:,.0f} items. Buy Vol: {buy_volume}")   # !!!!
                                    print(f"Profit: {profit_sell:,.2f} isk - {profit_sell_percentage:.2f}%")
                                except:
                                    pass

                            if DEBUG_MODE:
                                print(f'item_prices: {item_prices}')

                            if DEBUG_MODE == False:
                                print(".", end='' )

                            items_prices_parsed.append(item_prices)

                            if DEBUG_MODE:
                                print(f'Items Parsed Count: {len(items_prices_parsed)}')
                        else:
                            cnt += 1

                        # Отображение прогресса обновления данных.
#                        print(percentage_complete)
                        if percentage_complete % 10.068649885583524 == 0:
                            print(f"Loading Data: {int(percentage_complete)} %")


def lp_calculator():
    global items_quantity
#    global total_price

    cnt_items_counter_test = 0

    # Калькулятор себестоимости обмена LP на предмет
    for item in items_in_lp_store:
        cnt_items_counter_test += 1

        cnt_parsed_price = 0
        total_price = 0
        for component, quantity in item["lp_store_components"].items():
            for price in items_prices_parsed:
                if component == price[stations[0]['id']]["item_name"] and price[stations[0]['id']]["min_sell_price"] != None:
#                    if price[stations[0]['id']]["min_sell_price"] == None:
#                        print(f'None - {price[stations[0]["id"]]["item_name"]}')
                    if price[stations[0]['id']]["min_sell_price"] > 0:
                        total_price += price[stations[0]['id']]["min_sell_price"] * quantity
#                        print(f'Total Price: {total_price}')
#                        total_price += price[stations[0]["id"]]["min_sell_price"] * quantity
                        cnt_parsed_price += 1

                    # Добавление стоимости производства:
                    if "production_cost" in item and item["production_cost"] is not None:
                        total_price += item["production_cost"]

#                    try:
                        # Добавление стоимости Production (Производства). Реализовано через Try (ошибку).
                        # Не везде есть графа "Production" в списке. Пока, по другому не работает.
#                        if item["production_cost"] != False:
#                            total_price += item["production_cost"]
#                             print(f'Total Price : {total_price}')
#                    except:
#                        pass
#                    print(f'Total Price: {total_price}')
#                    print(f'item[isk_price]: {item["isk_price"]}')

                    if DEBUG_MODE:
                        try:
                            print(f'item test: {item}')
                            print(f'item lp_components: {len(item["lp_store_components"])}')
                            print(f'Price: {price}')
                            print(f'Component: {component}, price: {price[stations[0]["id"]]["min_sell_price"]} * quantity: {quantity}')
                            print(f'Total Price: {total_price}')
                            print(f'Cnt Parsed Price: {cnt_parsed_price}')
                        except:
                            print('Error: DEBUG_MODE - component == price[stations[0]["id"]]["item_name"]')

        total_price += item["isk_price"]       # Добавляем стоимость в isk

        if cnt_parsed_price == len(item["lp_store_components"]):
            items_quantity.append({"item_name": item["item_name"], "total_price": total_price})
            if DEBUG_MODE:
                print(f'Items quantity len: {len(items_quantity)}')
        else:
            print(f'Skip: {item["item_name"]}, Parsed price: {cnt_parsed_price}, len: {len(item["lp_store_components"])}')
#            if DEBUG_MODE:
#                print(f'Skip: {item["item_name"]}. Parsed price: {parsed_price}, len: {len(item["lp_store_components"])}')

        if DEBUG_MODE:
            print(f'Item: {item["item_name"]}. Total Price: {price[stations[0]["id"]]["min_sell_price"]} * {quantity} + {item["isk_price"]}, '
                  f'min_sell_price: {price[stations[0]["id"]]["min_sell_price"]} '
                  f'quantity: {quantity} '
                  f'item["isk_price"]: {item["isk_price"]} '
                  f'Item: {item["item_name"]}, '
                  f'Cost Price: {total_price:,.0f}, isk (ISK Price: {item["isk_price"]:,.0f} + LP ()) // Buy Income:  // Sell Income: \n')

    print(f'Items counter: {cnt_items_counter_test}')
    print(f'len(items_quantity): {len(items_quantity)}')
    print(f'Items LP Store Counter: {len(items_in_lp_store)}')
    print(f'Items Component Counter: {len(items_component_settings)}')
#    return items_quantity


if DEBUG_MODE:
    print('\n+++ Items +++')
    print()


def view_result():
    # Функция вывода информации
    global items_2_table
    global change_buy_lp_profit
    global change_sell_lp_profit
    global change_buy_volume

    cnt = 0
    index_number = 0

#    print(f'\nlen(items_in_lp_store): {len(items_in_lp_store)}')
#    print(f'len(items_prices_parsed): {len(items_prices_parsed)}')
#    print(f'len(items_quantity): {len(items_quantity)}')
#    print()

    for item in items_in_lp_store:
        for item_market in items_prices_parsed:
            if item["item_name"] == item_market[stations[0]["id"]]["item_name"]:
                for _ in items_quantity:                    # Цикл порядкового номера
#                    print(f'item: {item}')
#                    print(f'item_market: {item_market}')
#                    print(f'_: {_}')
#                    print(f'_["item_name"]: {item["item_name"]}')

                    if len(items_quantity) > cnt:
                        if items_quantity[cnt]["item_name"] == item["item_name"]:
                            # Формирование списка, и запись в переменную
                            item_name = item["item_name"]
                            item_buy_price = item_market[stations[0]["id"]]["max_buy_price"] * item["quantity"]
                            item_sell_price = item_market[stations[0]["id"]]["min_sell_price"]
                            item_total_price = items_quantity[cnt]["total_price"]
                            buy_lp_profit = ((item_market[stations[0]["id"]]["max_buy_price"] * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]

#                            print(f'Tests cnt:: {cnt}')
#                            print(f'len(items_quantity):: {len(items_quantity)}')

                            if DEBUG_MODE:
                                print(f'items_quantity[cnt]["item_name"]: {items_quantity[cnt]["item_name"]}, cnt:{cnt}, '
                                      f'item_name: {item_name}, '                                      
                                      f'item_buy_price: {item_buy_price} ({item_market[stations[0]["id"]]["max_buy_price"]} * {item["quantity"]}), '
                                      f'item_sell_price: {item_sell_price}, '
                                      f'item_total_price: {item_total_price}, '
                                      f'buy_lp_profit: {buy_lp_profit} - (({item_market[stations[0]["id"]]["max_buy_price"]} * {item["quantity"]}) - {items_quantity[cnt]["total_price"]}) // ({item["lp_price"]}), ', end='')
                            try:
                                sell_lp_profit = ((item_market[stations[0]["id"]]["min_sell_price"] * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]
#                                print(f'sell_lp_profit: {sell_lp_profit} (({item_market[stations[0]["id"]]["min_sell_price"]} * {item["quantity"]}) - {items_quantity[cnt]["total_price"]}) // ({item["lp_price"]})', end='')
                            except:
                                if DEBUG_MODE:
                                    # Except, если в маркете нет цены sell или buy для товара. Это значит, что скупили все ордера
                                    print(f'\nNo Sell prices for item: {item_market[stations[0]["id"]]["item_name"]}')
                                cnt += 1
                                continue

                            buy_lp_profit = int(buy_lp_profit * (1 - sales_tax))         # Отнимаем налог на продажу
                            sell_lp_profit = int(sell_lp_profit * (1 - sales_tax))       # Отнимаем налог на продажу
                            buy_volume = item_market[stations[0]["id"]]["best_buy_volume"]

                            if item_name and item_buy_price and item_sell_price and buy_lp_profit is not None:
                                # Проверка, что бы не добавлялись пустые слоты. В принципе, и без этой проверки все работало.
                                # Проблема с тем, что некоторые ордера неправильно считаются где-то в другом месте
                                items_2_table.append({
                                    "item_name": item_name,
                                    "item_buy_price": int(item_buy_price),
                                    "item_sell_price": int(item_sell_price),
                                    "item_total_price": item_total_price,
                                    "buy_lp_profit": buy_lp_profit,
                                    "sell_lp_profit": sell_lp_profit,
                                    "buy_volume": buy_volume,
                                })
                            else:
                                print(f'Skip - {item_name}')

                            if DEBUG_MODE:
                                try:
                                    print(f'\n{item["item_name"]} - Buy: {item_market[stations[0]["id"]]["max_buy_price"]:,.0f} isk // Sell: {item_market[stations[0]["id"]]["min_sell_price"]:,.0f} isk // Buy Profit: {((item_market[stations[0]["id"]]["max_buy_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]):,.0f} isk // Sell Profit: {(item_market[stations[0]["id"]]["min_sell_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]:,.2f} isk // \nBuy LP Profit: {((item_market[stations[0]["id"]]["max_buy_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]:,.0f} isk-lp // Sell LP Profit: {((item_market[stations[0]["id"]]["min_sell_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]:,.0f} isk-lp ')
                                except:
                                    print(f'Error: {item["item_name"]}')
                            cnt += 1
                        else:
                            pass
                    else:
                        pass
#                        print('Tests Counter... >')
#                            print(f'Сравнение: {items_quantity[cnt]["item_name"]} == {item["item_name"]} - {items_quantity[cnt]}')
    # Сортировка по Sell или Buy ордерам. Меняется в настройках
    items_2_table = sorted(items_2_table, key=lambda x: x[settings["sort_list"]], reverse=True)
#    print(f'Tests: len(items_2_table): {len(items_2_table)}')

    save_json(items_2_table)

    print()
    print('\n===========================================================================================================')
    print(f'Название предмета: {39 * " "} Buy: {5 * " "} Buy Volume: {11 * " "} Sell:')

    for item_info in items_2_table:
        if settings["filter_min_isk_per_lp"] <= item_info[settings["sort_list"]]: #item_info["sell_lp_profit"]:        # Проверка на минимальное значение isk pf 1 LP:

            if items_2_table_last_request:
                # Вычисление изменений в данных (Buy, Sell, Volume).
                for item_previous_request in items_2_table_last_request:
                    if item_info["item_name"] == item_previous_request["item_name"]:

                        if item_info['buy_lp_profit'] == item_previous_request["buy_lp_profit"] or item_previous_request["buy_lp_profit"] == None:
                            change_buy_lp_profit = "-"
                        elif item_info['buy_lp_profit'] > item_previous_request["buy_lp_profit"]:
                            change_buy_lp_profit = "+ " + str(int(item_info['buy_lp_profit'] - item_previous_request["buy_lp_profit"]))
                        elif item_info['buy_lp_profit'] < item_previous_request["buy_lp_profit"]:
                            change_buy_lp_profit = "- " + str(int(item_previous_request["buy_lp_profit"] - item_info['buy_lp_profit']))

                        if item_info['sell_lp_profit'] == item_previous_request["sell_lp_profit"] or item_previous_request["sell_lp_profit"] == None:
                            change_sell_lp_profit = "-"
                        elif item_info['sell_lp_profit'] > item_previous_request["sell_lp_profit"]:
                            change_sell_lp_profit = "+ " + str(int(item_info['sell_lp_profit'] - item_previous_request["sell_lp_profit"]))
                        elif item_info['sell_lp_profit'] < item_previous_request["sell_lp_profit"]:
                            change_sell_lp_profit = "- " + str(int(item_previous_request["sell_lp_profit"] - item_info['sell_lp_profit']))

                        if item_info['buy_volume'] == item_previous_request["buy_volume"] or item_previous_request["buy_volume"] == None:
                            change_buy_volume = "-"
                        elif item_info['buy_volume'] > item_previous_request["buy_volume"]:
                            change_buy_volume = "+ " + str(int(item_info['buy_volume'] - item_previous_request["buy_volume"]))
                        elif item_info['buy_volume'] < item_previous_request["buy_volume"]:
                            change_buy_volume = "- " + str(int(item_previous_request["buy_volume"] - item_info['buy_volume']))
            else:
                change_buy_lp_profit = "-"
                change_sell_lp_profit = "-"
                change_buy_volume = "-"

            # Вывод информации
            if index_number >= sort_list_counter_2_view and sort_list_counter_2_view != 0:
                print('Break.')
                break

            index_number += 1                            # Счётчик порядкового номера

            # Ограничение кол-ва выводимых позиций.
            if settings['lp_store_parser_number_view_items'] != 'all' and settings['lp_store_parser_number_view_items'] == index_number - 1:
                print('Break..')
                break

            print(f"{index_number}. {item_info['item_name']}: {(54 - len(item_info['item_name'] + str(index_number))) * ' '} "
                  f"{color_lp_profit(item_info['buy_lp_profit'])} ({change_buy_lp_profit})     [{item_info['buy_volume']}] ({change_buy_volume}){(20 - (len(str(item_info['buy_lp_profit'])) + len(str(item_info['buy_volume'])) + len(change_buy_lp_profit))) * ' '} "
                  f"{color_lp_profit(item_info['sell_lp_profit'])} ({change_sell_lp_profit})")

    if DEBUG_MODE:
        print(f'Items_2_table len list: {len(items_2_table)}')
#        for i in items_2_table:
#            print(i)
#    return items_2_table


#if DEBUG_MODE:
#    print('+++ Persed Items +++')
#    print(items_prices_parsed)


def check_time_limit():
    """
    Функция для проверки лимитов по времени.
    Используется для распространения скрипта через интернет
    """
    end_datetime = datetime.datetime(2024, 12, 31, 11, 0)
    current_datetime = datetime.datetime.utcnow()
    if current_datetime > end_datetime:
        print("\n\nThe time for using the program has expired. \nThe program will be closed after 1 minute.")
        time.sleep(60)
        sys.exit()
    else:
        return True


if __name__ == "__main__":
    while True:
        if check_time_limit():

            # Обнуление параметров
    #        items = items_faction_wars_state_protectorate + items_component
            items = items_component_settings
            items_prices_parsed = []
            items_quantity = []
            items_2_table = []
            total_price = 0

            try:
                items_prices()
                lp_calculator()
                view_result()
            except requests.exceptions.ConnectionError as error:
                print(f'\n\nConnection Error:')
                print(f'Most likely the number of requests to the server has been exceeded. '
                      f'\nSo far, no additional information is available.')
                print(f'{error}')

            print(f'\nTime: {time.time() - start_time:,.2f} sec')
    #        print(f'Update after {auto_time_update} min.')
    #        time.sleep(auto_time_update * 60)
            menu_console_interface()

            items_2_table_last_request = items_2_table


#items_prices()
#lp_calculator()
#view_result()


if DEBUG_MODE:
    print('\nPass')
print(f'\nTime: {time.time() - start_time:,.2f} sec')
