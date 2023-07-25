import requests
import time

from items_faction_wars import items_faction_wars_state_protectorate, items_component
from colors import color_lp_profit
from settings import debug_mode


start_time = time.time()

#items_faction_wars_state_protectorate = list(items_faction_wars_state_protectorate)

items = items_faction_wars_state_protectorate + items_component
items_prices_parsed = []
items_quantity = []
items_2_table = []
total_price = 0


print(f'Items Components Count: {len(items)}')
print(f'Items Market Count: {len(items_faction_wars_state_protectorate)}', end='')


def get_item_prices(item_id, item_name, region_id, region_name, station_id, station_name, sales_tax):
    url = "https://esi.evetech.net/latest/markets/{}/orders/?datasource=tranquility&order_type=all&page=1&type_id={}"

    headers = {
        'User-Agent': 'your_user_agent'
    }

    prices = {}

    region_url = url.format(region_id, item_id)
    response = requests.get(region_url, headers=headers)

    if response.status_code == 200:
        orders = response.json()

        filtered_orders = [order for order in orders if order["location_id"] == station_id]

        sell_prices = [order["price"] for order in filtered_orders if order["is_buy_order"] is False]
        buy_prices = [order["price"] for order in filtered_orders if order["is_buy_order"] is True]

        min_sell_price = min(sell_prices) if sell_prices else None
        max_buy_price = max(buy_prices) if buy_prices else None

        trade_volume = sum(order["volume_remain"] for order in filtered_orders if not order["is_buy_order"])

        if min_sell_price is not None and max_buy_price is not None:
            buy_price = min_sell_price
            profit_sell = buy_price - max_buy_price
            profit_sell_percentage = (profit_sell / buy_price) * 100

            prices[station_id] = {
                "region_name": region_name,
                "station_name": station_name,
                "item_name": item_name,
                "min_sell_price": min_sell_price,
                "max_buy_price": max_buy_price,
                "trade_volume": trade_volume,
                "profit_sell": profit_sell,
                "profit_sell_percentage": profit_sell_percentage
            }

    else:
        print(f"Ошибка при получении цен на товар '{item_name}' в регионе '{region_name}': {response.status_code}")

    return prices


regions = [
    {"id": 10000002, "name": "The Forge"},
#    {"id": 10000043, "name": "Domain"}
]

stations = [
    {"id": 60003760, "name": "Jita 4-4 - Caldari Navy Assembly Plant"},
#    {"id": 60008494, "name": "Amarr VIII (Oris) - Emperor Family Academy"}
]

sales_tax = 0.05  # Здесь нужно указать комиссию на продажу (например, 0.05 для 5%)


def items_prices():
    # Парсим цены по разным товарам
    global items_prices_parsed

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
    #                print(f"\nТовар: '{item_name}' в регионе '{region_name}' на станции '{station_name}':")
                    for station_id, station_prices in item_prices.items():
                        if station_prices:
                            if debug_mode:
                                print(f"\nТовар: '{item_name}' в регионе '{region_name}' на станции '{station_name}':")

                            min_sell_price = station_prices["min_sell_price"]
                            max_buy_price = station_prices["max_buy_price"]
                            trade_volume = station_prices["trade_volume"]
                            profit_sell = station_prices["profit_sell"]
                            profit_sell_percentage = station_prices["profit_sell_percentage"]

                            if debug_mode:
                                print(f"Sell Price: {min_sell_price:,.0f}, Buy Price: {max_buy_price:,.0f}")
                                print(f"Торговый объем - {trade_volume:,.0f} items")
                                print(f"Profit: {profit_sell:,.2f} isk - {profit_sell_percentage:.2f}%")
                            if debug_mode == False:
                                print(".", end='' )
                            items_prices_parsed.append(item_prices)

    ###                        print(f"Процент прибыли от продажи - {profit_sell_percentage:.2f}%")
    ##                    if station_prices:
    ##                        id["id"].append(item_name)
                        else:
                            pass
    #                        print(f"Цены недоступны для станции '{station_name}'")
    ##                        print('.', end="")
                else:
                    pass
    #                print(f"Не удалось получить цены на товар '{item_name}' в регионе '{region_name}' на станции '{station_name}'")


#items_prices()


def lp_calculator():
    global items_quantity
    global total_price
    # Калькулятор себестоимости обмена LP на предмет
    #print('\nComponents')
    #for item in items_component:                                # Тут не понятно. Вроде работает, но возможно нужно добавить еще один цикл
    for item in items_faction_wars_state_protectorate:
    #    print(f'Item: {j["item_name"]}')
        for component, quantity in item["lp_store_components"].items():
    #        print('Check')
    #        print(quantity)
            for price in items_prices_parsed:
                if component == price[60003760]["item_name"]:
                    if debug_mode:
                        print(f'Component {component} - Price: {price[60003760]["min_sell_price"]}')
                    total_price += price[60003760]["min_sell_price"] * quantity
                    try:
                        # Добавление стоимости производства, если оно есть
                        if item["production_cost"] or item["production_cost"] == None:
                            total_price += item["production_cost"]
                    except:
                        pass

        total_price += item["isk_price"]       # Добавляем стоимость в isk
        isk_price = item["isk_price"]
    #       print(isk_price)
    #       items_quantity.extend([j["item_name"], total_price])
        items_quantity.append({"item_name": item["item_name"], "total_price": total_price})
        total_price = 0
        if debug_mode:
            print(f'Item: {item["item_name"]}, Cost Price: {total_price:,.0f} isk (ISK: {item["isk_price"]:,.0f} + LP ()) // Buy Income:  // Sell Income: ')

#lp_calculator()


if debug_mode:
    print('\n+++ Items +++')


def view_result():
    # Функция вывода информации
    global items_2_table

    cnt = 0                             # Counter для алгоритма
    index_number = 0

    for item in items_faction_wars_state_protectorate:
    #    print('+')
    #    print(item)
        for j_parsed in items_prices_parsed:
    #        print(j)
    #        print(j[60003760]["max_buy_price"])
    #        print(f'{j[60003760]["item_name"]} - {j[60003760]["max_buy_price"]}')
            if item["item_name"] == j_parsed[60003760]["item_name"]:
    #            print('item')
    #            print(j_parsed[60003760]["item_name"])
    #            print(item["item_name"])
                for item_counter in items_quantity:                    # Добавляю цикл, чтобы узнать порядок в списке
    #                cnt = 0
    #                print('item_counter')
    #                print(item_counter)
    #                print(counter["item_name"])
    #                print(items_quantity[cnt]["item_name"])
                    if len(items_quantity) > cnt:
                        if items_quantity[cnt]["item_name"] == item["item_name"]:
                            # Формирование списка, и запись в переменную
                            item_name = item["item_name"]
    #                        print(item_name)
                            item_buy_price = j_parsed[60003760]["max_buy_price"] * item["quantity"]
    #                        print(item_buy_price)
                            item_sell_price = j_parsed[60003760]["min_sell_price"]
    #                        print(item_sell_price)
                            item_total_price = items_quantity[cnt]["total_price"]
    #                        print(item_sell_price)
                            buy_lp_profit = ((j_parsed[60003760]["max_buy_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]
                            sell_lp_profit = ((j_parsed[60003760]["min_sell_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]
    #                        items_2_table.append({"item_name": item_name, "item_buy_price": item_buy_price, "item_sell_price": item_sell_price, "item_total_price": item_total_price, "buy_lp_profit": buy_lp_profit, "sell_lp_profit": sell_lp_profit})
                            items_2_table.append({
                                "item_name": item_name,
                                "item_buy_price": item_buy_price,
                                "item_sell_price": item_sell_price,
                                "item_total_price": item_total_price,
                                "buy_lp_profit": buy_lp_profit,
                                "sell_lp_profit": sell_lp_profit
                            })

    #                        print("\nTest")
    #                        print(items_2_table)
    #                    print("+++")
    #                    print(item)
    #                    print(items_quantity[cnt-1]["total_price"])
    #                        print(j_parsed[60003760])
    #                    print(f'cnt: {cnt}')
    #                    print(f'Price: {items_quantity[cnt-1]["total_price"]}')
    #                        print(j_parsed[60003760])
    #                        print(item_buy_price)
    #                        print(item_total_price)
    #                        print(item_buy_price - item_total_price)
    #                        print(item)
    #                        print(item["quantity"])
                            if debug_mode:
                                print(f'\n{item["item_name"]} - Buy: {j_parsed[60003760]["max_buy_price"]:,.0f} isk // Sell: {j_parsed[60003760]["min_sell_price"]:,.0f} isk // Buy Profit: {((j_parsed[60003760]["max_buy_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]):,.0f} isk // Sell Profit: {(j_parsed[60003760]["min_sell_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]:,.2f} isk // \nBuy LP Profit: {((j_parsed[60003760]["max_buy_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]:,.0f} isk-lp // Sell LP Profit: {((j_parsed[60003760]["min_sell_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]:,.0f} isk-lp ')
                            cnt += 1

    # Сортировка по Buy
    #items_2_table = sorted(items_2_table, key=lambda x: x["buy_lp_profit"], reverse=True)
    # Сортировка по Sell
    items_2_table = sorted(items_2_table, key=lambda x: x["sell_lp_profit"], reverse=True)

    print()
    print('==========================================================================================')
    print('\nОтсортированный список:')

    for item_info in items_2_table:
        index_number += 1                            # Счётчик порядкового номера
        print(f"{index_number}. {item_info['item_name']}: {(44 - len(item_info['item_name'] + str(index_number))) * ' '} "
              f"Buy LP-isk: {color_lp_profit(item_info['buy_lp_profit'])} {(8 - len(str(item_info['buy_lp_profit']))) * ' '} "
              f"Sell LP-isk: {color_lp_profit(item_info['sell_lp_profit'])}")
    #    print(f"Item Name: {item_info['item_name']}")
    #    print(f"Item Buy Price: {item_info['item_buy_price']}")
    #    print(f"Item Sell Price: {item_info['item_sell_price']}")
    #    print(f"Item Total Price: {item_info['item_total_price']}")
    #    print(f"Buy LP Profit: {item_info['buy_lp_profit']}")
    #    print(f"Sell LP Profit: {item_info['sell_lp_profit']}")
    #    print()


while True:
    # Обнуление параметров
    items = items_faction_wars_state_protectorate + items_component
    items_prices_parsed = []
    items_quantity = []
    items_2_table = []
    total_price = 0

    items_prices()
    lp_calculator()
    view_result()
    time.sleep(60)


items_prices()
lp_calculator()
view_result()



if debug_mode:
    print('\nPass')
print(f'\nTime: {time.time() - start_time:,.2f} sec')

#print(items_prices_parsed)
