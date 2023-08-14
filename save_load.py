import csv
import json
import datetime

import colors
from colors import color_lp_profit


#data = [
#    {"name": "Алиса", "age": 25, "city": "Нью-Йорк"},
#    {"name": "Боб", "age": 30, "city": "Лос-Анджелес"},
#    {"name": "Чарли", "age": 22, "city": "Чикаго"}
#]


csv_file_path = "lp_state_protectorate.csv"
json_file_path = "lp_state_protectorate.json"


def save_csv(items_2_table):
    # Запись данных в CSV файл с кодировкой UTF-8
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["item_name", "item_buy_price", "item_sell_price", "item_total_price",
                      "buy_lp_profit", "sell_lp_profit", "buy_volume"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        writer.writeheader()  # Запись заголовка

        for row in items_2_table:
            writer.writerow(row)

        print('+')
        file.write(f"Time of creation: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def save_json(items_2_table):
    # Запись данных в json файл с кодировкой UTF-8
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(items_2_table, json_file, ensure_ascii=False)


def load_json():
    index_number = 0

    try:
        # Чтение данных из JSON файла с кодировкой UTF-8
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            items_2_table = json.load(json_file)
            print(f'Название предмета: {35 * " "} isk-LP {5 * " "} Buy Vol: {6 * " "} isk-LP Profit')

            for item_info in items_2_table:
                index_number += 1
                print(
                    f"{index_number}. {item_info['item_name']}: {(50 - len(item_info['item_name'] + str(index_number))) * ' '} "
                    f"Buy: {colors.color_lp_profit(item_info['buy_lp_profit'])} {(7 - len(str(item_info['buy_lp_profit']))) * ' '}[{item_info['buy_volume']}] {(13 - len(str(item_info['buy_volume']))) * ' '}"
                    f"Sell: {colors.color_lp_profit(item_info['sell_lp_profit'])}")

        return items_2_table
    except FileNotFoundError:
        return []



def load_csv():
    # Функция для чтения данных из csv файла с данными
    index_number = 0

    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        last_line = lines[-1].strip()  # Получаем последнюю строку и удаляем символы перевода строки

        for item_info in lines:
            index_number += 1
            print(item_info)
            try:
                print(
                    f"{index_number}. {item_info['item_name']}: {(45 - len(item_info['item_name'] + str(index_number))) * ' '} "
                    f"Buy: {color_lp_profit(item_info['buy_lp_profit'])} ({change_buy_lp_profit}) [{item_info['buy_volume']}] ({change_buy_volume}){(20 - (len(str(item_info['buy_lp_profit'])) + len(str(item_info['buy_volume'])) + len(change_buy_lp_profit))) * ' '} "
                    f"Sell: {color_lp_profit(item_info['sell_lp_profit'])} ({change_sell_lp_profit})")
            except:
                pass
#            print(item_info)

        if last_line.startswith("Time of creation:"):
            time_str = last_line.split("Time of creation:")[1].strip()
            time_format = "%Y-%m-%d %H:%M:%S"
            last_creation_time = datetime.datetime.strptime(time_str, time_format)
            return last_creation_time
        else:
            return None
#            data.append(row)



#save_csv(items_2_table)
#load_csv()
#load_json()
