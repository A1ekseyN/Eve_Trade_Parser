# pyinstaller -F --icon=icon_parser.ico main.py
# pyinstaller -F --icon=icon_parser.ico main.py --hidden-import=pkg_resources

import requests
import json
import time
from tqdm import tqdm

from items_all_market import items_eve
from items_manual import items_sorted_manual
from items_ships import items_ships
from items_modules import items_modules


# https://www.adam4eve.eu/info_locations.php

version = "0.0.1b"
start_time = time.time()

items = items_eve                           # items_sorted_manual         # Список items, которые анализируются из рынка
items = items_ships                         # Переменная со списком кораблей
items = items_modules                       # Переменная с дорогими модулями
items = items_ships + items_modules

dump_orders_all = []
filter_price_min = 200000                   # Фильтр минимальной цены
#filter_price_min = 10000000                   # Фильтр минимальной цены

sales_tax = 0.05                            # Здесь нужно указать комиссию на продажу (например, 0.05 для 5%)


print(f'Items Count: {len(items)}')

# Фильтр, который исключает ключевые слова
excluded_keywords = ['day', 'Days', 'Serenity', 'background', 'Non-interactable', 'non-interactable']
items = [item for item in items if not any(keyword in item['name'] for keyword in excluded_keywords)]
print(f'Filtered Items Count: {len(items)}')


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
    {"id": 60003760, "name": "Jita 4-4"},
#    {"id": 60008494, "name": "Amarr VIII (Oris) - Emperor Family Academy"}
]

# Анализируем товары, прогресс будет отслеживаться только по товарам
while True:
#    for item in items:
    for item in tqdm(items, desc=f"Analyzing items {regions[0]['name']}", colour="green"):
        item_id = item["id"]
        item_name = item["name"]

        # Проходим по каждому региону (в данном случае выбран только "The Forge")
        region = regions[0]  # Заранее выбираем нужный регион (например, Jita)
        region_id = region["id"]
        region_name = region["name"]

        # Проходим по каждой станции (например, Jita 4-4)
        station = stations[0]  # Заранее выбираем нужную станцию (например, Jita 4-4)
        station_id = station["id"]
        station_name = station["name"]

        # Получаем цены на товар
        item_prices = get_item_prices(item_id, item_name, region_id, region_name, station_id, station_name, sales_tax)

        # Если есть данные по ценам и они соответствуют фильтрам
        if item_prices and station_id in item_prices:
            station_prices = item_prices[station_id]
            if station_prices["profit_sell_percentage"] <= 0.1 and station_prices["min_sell_price"] >= filter_price_min:
                print(f"\nТовар [id: {item['id']}]: '{item_name}' в регионе '{region_name}' на станции '{station_name}':")
                min_sell_price = station_prices["min_sell_price"]
                max_buy_price = station_prices["max_buy_price"]
                trade_volume = station_prices["trade_volume"]

                profit_sell = station_prices["profit_sell"]
                profit_sell_percentage = station_prices["profit_sell_percentage"]

                print(f"Sell Price: {min_sell_price:,.0f}, Buy Price: {max_buy_price:,.0f}")
    #            print(f"Volume: - {trade_volume:,.0f} items")
    #            print(f"Profit: {profit_sell:,.2f} isk - {profit_sell_percentage:.2f}%")
                print()

        if station_prices:
            dump_orders_all.append(item_prices)


#with open("output.txt", "w", encoding="utf-8") as file:
#    json.dump(dump_orders_all, file)
#    print("File saved output.txt")


print(f'\nTime: {time.time() - start_time:,.2f} sec')
