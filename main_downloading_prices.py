import requests
import csv
import time
from tqdm import tqdm
from collections import defaultdict

from items_all_market import items_eve
from items_manual import items_sorted_manual
from items_ships import items_ships
from items_modules import items_modules


class EveMarketParser:
    def __init__(self, items, locations, user_agent='your_user_agent', format_large_numbers=False):
        self.locations = locations
        self.user_agent = user_agent
        self.format_large_numbers = format_large_numbers
        self.apply_price_limit = False                              # Вкл/выкл лимит на цену
        self.price_limit = 1000000                                  # Price limit to write csv
        self.max_items = 100000                                         # Количество Items по которым делаются запросы
        self.items = self.filter_items(items)[:self.max_items]      # Ограничение на количество
        self.dump_orders_all = defaultdict(lambda: {
            "price_sell_jita": None,
            "price_buy_jita": None,
            "price_sell_amarr": None,
            "price_buy_amarr": None,
            "sell_vol_jita": 0,
            "buy_vol_jita": 0,
            "sell_vol_amarr": 0,
            "buy_vol_amarr": 0,
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
                print(f"Connection error occurred: {e}. Retrying in 15 seconds...")
                time.sleep(15)

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
                            self.dump_orders_all[item_id][f"buy_vol_{loc_key}"] = price["volume_remain"]
                    else:
                        if self.dump_orders_all[item_id][f"price_sell_{loc_key}"] is None or price["price"] < self.dump_orders_all[item_id][f"price_sell_{loc_key}"]:
                            self.dump_orders_all[item_id][f"price_sell_{loc_key}"] = price["price"]
                            self.dump_orders_all[item_id][f"sell_vol_{loc_key}"] = price["volume_remain"]

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

    def format_number(self, number):
        """Форматирует большие числа, используя тысячи и миллионы. (Тысяча - K, Миллион - M)"""
        try:
            if number is None:  # Пропускаем если нет данных.
                return "N/A"

            number = float(number)  # Convert to float to handle numbers represented as strings
            if number >= 1_000_000:
                return f"{number / 1_000_000:.2f} M"
            elif number >= 1_000:
                return f"{number / 1_000:.2f} K"
            else:
                return f"{number:.2f}"
        except ValueError:
            # Handle cases where the value cannot be converted to a number
            return str(number)

    def save_to_csv(self, filename, sort_by_column='jita_to_amarr_sell_sell_%'):
        keys = [
            "id", "item_name",
            "price_sell_jita", "price_buy_jita", "sell_vol_jita", "buy_vol_jita", "station_price_diff_jita_%",
            "price_sell_amarr", "price_buy_amarr", "sell_vol_amarr", "buy_vol_amarr",
            "station_price_diff_amarr_%",
            "jita_to_amarr_sell_sell_%", "jita_to_amarr_buy_buy_%", "jita_to_amarr_sell_buy_%",
            "jita_to_amarr_buy_sell_%"
        ]

        # Фильтруем данные по сумме объемов в столбиках C, D, I, J, если флаг apply_volume_limit включен
        if self.apply_price_limit:
            filtered_data = [
                item for item in self.dump_orders_all.values()
                if (
                       (item.get("sell_vol_jita", 0) or 0) +
                       (item.get("buy_vol_jita", 0) or 0) +
                       (item.get("sell_vol_amarr", 0) or 0) +
                       (item.get("buy_vol_amarr", 0) or 0)
                   ) >= self.price_limit
            ]
        else:
            filtered_data = list(self.dump_orders_all.values())

        # Сортировка данных по указанной колонке
        sorted_data = sorted(
            filtered_data,
            key=lambda x: x.get(sort_by_column, float('-inf')) if x.get(sort_by_column) is not None else float('-inf'),
            reverse=True  # Сортировка по убыванию
        )

        # Столбцы с денежными значениями
        currency_columns = {"price_sell_jita", "price_buy_jita", "sell_vol_jita", "buy_vol_jita",
                            "price_sell_amarr", "price_buy_amarr", "sell_vol_amarr", "buy_vol_amarr"}

        # Запись в CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            for item_data in sorted_data:
                # Форматируем значения, если включено format_large_numbers
                formatted_data = {
                    key: (
                        f"{self.format_number(value)}" if key in currency_columns and isinstance(value, (int, float))
                        else value
                    )
                    for key, value in item_data.items()
                }
                writer.writerow(formatted_data)
        print(f"File saved: {filename}")


if __name__ == "__main__":
    items = [
        {"id": 34, "name": "Tritanium"},
        {"id": 35, "name": "Pyerite"}
    ]

#    items = items_eve               # Все items из маркета
    items = items_ships             # Корабли
#    items = items_sorted_manual     # Items отсортированные в ручную
#    items = items_modules           # Items - Вещи из спписка составленного в ручную. Модули
#    items = items_ships + items_modules

    locations = [
        {"region_id": 10000002, "region_name": "The Forge", "station_id": 60003760, "station_name": "Jita 4-4"},
        {"region_id": 10000043, "region_name": "Domain", "station_id": 60008494, "station_name": "Amarr VIII (Oris) - Emperor Family Academy"}
    ]

    parser = EveMarketParser(items, locations, format_large_numbers=True)
    parser.collect_data()
    parser.save_to_csv("output_prices_filtered.csv", sort_by_column="jita_to_amarr_sell_sell_%")
