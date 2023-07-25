
import requests
import json
import time

from items_all_market import items_eve


# https://www.adam4eve.eu/info_locations.php

version = "0.0.1a"
start_time = time.time()

items = items_eve
dump_orders_all = []


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


# Генератор id
#items = [{'id': id, 'name': id} for id in range(1, 80001)]
#id = {'id':[]}


regions = [
    {"id": 10000002, "name": "The Forge"},
#    {"id": 10000043, "name": "Domain"}
]

stations = [
    {"id": 60003760, "name": "Jita 4-4 - Caldari Navy Assembly Plant"},
#    {"id": 60008494, "name": "Amarr VIII (Oris) - Emperor Family Academy"}
]

sales_tax = 0.05  # Здесь нужно указать комиссию на продажу (например, 0.05 для 5%)

for item in items:
    item_id = item["id"]
    item_name = item["name"]

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
                    if station_prices and station_prices["profit_sell_percentage"] <= 0.1:
                        print(f"\nТовар: '{item_name}' в регионе '{region_name}' на станции '{station_name}':")

                        min_sell_price = station_prices["min_sell_price"]
                        max_buy_price = station_prices["max_buy_price"]
                        trade_volume = station_prices["trade_volume"]
                        profit_sell = station_prices["profit_sell"]
                        profit_sell_percentage = station_prices["profit_sell_percentage"]

                        print(f"Sell Price: {min_sell_price:,.0f}, Buy Price: {max_buy_price:,.0f}")
                        print(f"Торговый объем - {trade_volume:,.0f} items")
                        print(f"Profit: {profit_sell:,.2f} isk - {profit_sell_percentage:.2f}%")
###                        print(f"Процент прибыли от продажи - {profit_sell_percentage:.2f}%")
##                    if station_prices:
##                        id["id"].append(item_name)
                    else:
                        pass
#                        print(f"Цены недоступны для станции '{station_name}'")
##                        print('.', end="")
                    if station_prices:
                        dump_orders_all.append(item_prices)
#                        print(item_prices)
#                        print('+')
#                        print(dump)
            else:
                pass
#                print(f"Не удалось получить цены на товар '{item_name}' в регионе '{region_name}' на станции '{station_name}'")



with open("output.json", "w", encoding="utf-8") as file:
    json.dump(dump_orders_all, file)
    print("File saved output.json")

with open("output.txt", "w", encoding="utf-8") as file:
    json.dump(dump_orders_all, file)
    print("File saved output.txxt")


#print(id)
print(f'\nTime: {time.time() - start_time} sec')

