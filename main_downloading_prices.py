import requests
import csv
import time
from tqdm import tqdm
from collections import defaultdict

from items_all_market import items_eve
from items_manual import items_sorted_manual

class EveMarketParser:
    def __init__(self, items, locations, user_agent='your_user_agent'):
        self.items = self.filter_items(items)
        self.locations = locations
        self.user_agent = user_agent
        self.dump_orders_all = defaultdict(lambda: {
            "price_sell_jita": None,
            "price_buy_jita": None,
            "price_sell_amarr": None,
            "price_buy_amarr": None,
            "sell_volume_jita": 0,
            "buy_volume_jita": 0,
            "sell_volume_amarr": 0,
            "buy_volume_amarr": 0,
            "station_price_diff_jita_%": None,
            "station_price_diff_amarr_%": None,
            "jita_to_amarr_sell_sell_%": None,
            "jita_to_amarr_buy_buy_%": None,
            "jita_to_amarr_sell_buy_%": None,
            "jita_to_amarr_buy_sell_%": None
        })

    @staticmethod
    def filter_items(items):
        excluded_keywords = ['day', 'Days', 'Serenity', 'background', 'Non-interactable', 'non-interactable']
        return [item for item in items if not any(keyword in item['name'] for keyword in excluded_keywords)]

    def get_item_prices(self, item_id, item_name, location):
        url = f"https://esi.evetech.net/latest/markets/{location['region_id']}/orders/?datasource=tranquility&order_type=all&page=1&type_id={item_id}"
        headers = {
            'User-Agent': self.user_agent
        }

        while True:
            try:
                response = requests.get(url, headers=headers, timeout=60)
                prices = []

                if response.status_code == 200:
                    orders = response.json()
                    filtered_orders = [order for order in orders if order["location_id"] == location['station_id']]

                    for order in filtered_orders:
                        prices.append({
                            "id": item_id,
                            "item_name": item_name,
                            "region_name": location['region_name'],
                            "station_name": location['station_name'],
                            "price": order["price"],
                            "volume_remain": order["volume_remain"],
                            "is_buy_order": order["is_buy_order"]
                        })
                else:
                    print(f"Ошибка при получении цен на товар '{item_name}' в регионе '{location['region_name']}': {response.status_code}")

                return prices
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error occurred: {e}. Retrying in 60 seconds...")
                time.sleep(60)

    def collect_data(self):
        for item in tqdm(self.items, desc="Collecting item data", colour='green'):
            item_id = item["id"]
            item_name = item["name"]

            for location in self.locations:
                item_prices = self.get_item_prices(item_id, item_name, location)
                loc_key = 'jita' if location['station_name'] == 'Jita 4-4' else 'amarr'

                for price in item_prices:
                    if price["is_buy_order"]:
                        if self.dump_orders_all[item_id][f"price_buy_{loc_key}"] is None or price["price"] > self.dump_orders_all[item_id][f"price_buy_{loc_key}"]:
                            self.dump_orders_all[item_id][f"price_buy_{loc_key}"] = price["price"]
                            self.dump_orders_all[item_id][f"buy_volume_{loc_key}"] = price["volume_remain"]
                    else:
                        if self.dump_orders_all[item_id][f"price_sell_{loc_key}"] is None or price["price"] < self.dump_orders_all[item_id][f"price_sell_{loc_key}"]:
                            self.dump_orders_all[item_id][f"price_sell_{loc_key}"] = price["price"]
                            self.dump_orders_all[item_id][f"sell_volume_{loc_key}"] = price["volume_remain"]

            # Update percentage difference
            self.dump_orders_all[item_id][f"station_price_diff_jita_%"] = self.calculate_price_difference_percent(
                self.dump_orders_all[item_id]["price_sell_jita"], self.dump_orders_all[item_id]["price_buy_jita"]
            )
            self.dump_orders_all[item_id][f"station_price_diff_amarr_%"] = self.calculate_price_difference_percent(
                self.dump_orders_all[item_id]["price_sell_amarr"], self.dump_orders_all[item_id]["price_buy_amarr"]
            )

            # Add item name for each entry
            self.dump_orders_all[item_id]["id"] = item_id
            self.dump_orders_all[item_id]["item_name"] = item_name

            # Calculate potential profits in percentage
            self.dump_orders_all[item_id]["jita_to_amarr_sell_sell_%"] = self.calculate_potential_profit_percent(
                self.dump_orders_all[item_id]["price_sell_jita"], self.dump_orders_all[item_id]["price_sell_amarr"]
            )
            self.dump_orders_all[item_id]["jita_to_amarr_buy_buy_%"] = self.calculate_potential_profit_percent(
                self.dump_orders_all[item_id]["price_buy_jita"], self.dump_orders_all[item_id]["price_buy_amarr"]
            )
            self.dump_orders_all[item_id]["jita_to_amarr_sell_buy_%"] = self.calculate_potential_profit_percent(
                self.dump_orders_all[item_id]["price_sell_jita"], self.dump_orders_all[item_id]["price_buy_amarr"]
            )
            self.dump_orders_all[item_id]["jita_to_amarr_buy_sell_%"] = self.calculate_potential_profit_percent(
                self.dump_orders_all[item_id]["price_buy_jita"], self.dump_orders_all[item_id]["price_sell_amarr"]
            )

    def calculate_price_difference_percent(self, price_sell, price_buy):
        if price_sell is None or price_buy is None or price_sell == 0:
            return None
        else:
            return round(((price_sell - price_buy) / price_sell) * 100, 2)

    def calculate_potential_profit_percent(self, price_buy, price_sell):
        if price_buy is None or price_sell is None or price_buy == 0:
            return None
        else:
            return round(((price_sell - price_buy) / price_buy) * 100, 2)

    def save_to_csv(self, filename):
        keys = [
            "id", "item_name",
            "price_sell_jita", "price_buy_jita", "sell_volume_jita", "buy_volume_jita", "station_price_diff_jita_%",
            "price_sell_amarr", "price_buy_amarr", "sell_volume_amarr", "buy_volume_amarr", "station_price_diff_amarr_%",
            "jita_to_amarr_sell_sell_%", "jita_to_amarr_buy_buy_%", "jita_to_amarr_sell_buy_%", "jita_to_amarr_buy_sell_%"
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            for item_id, item_data in self.dump_orders_all.items():
                writer.writerow(item_data)
        print(f"File saved: {filename}")

if __name__ == "__main__":
    items = [
        {"id": 34, "name": "Tritanium"},
        {"id": 35, "name": "Pyerite"}
    ]

    items = items_eve               # Все items из маркета
#    items = items_sorted_manual     # Items отсортированные в ручную

    locations = [
        {"region_id": 10000002, "region_name": "The Forge", "station_id": 60003760, "station_name": "Jita 4-4"},
        {"region_id": 10000043, "region_name": "Domain", "station_id": 60008494, "station_name": "Amarr VIII (Oris) - Emperor Family Academy"}
    ]

    parser = EveMarketParser(items, locations)
    parser.collect_data()
    parser.save_to_csv("output_prices_filtered.csv")
