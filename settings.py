version = "0.0.1d"
DEBUG_MODE = False
colors = True    # Включает и выключает цветовую индикацию. Цвета нужно выключать, когда программа компилируется в *.exe


settings = {"sort_list": "sell_lp_profit",
            "lp_store_parser_number_view_items": "all",
#            "sort_list_counter_2_view": "0",
#            "filter_lp_number": "None",
            "filter_min_isk_per_lp": -200000,
            "market_region": "jita",
            "sales_tax": "0.05", }


# Загрузка и сохранение файла настрое
def save_settings(settings):
    with open("settings.txt", "w") as file:
        for key, value in settings.items():
            file.write(f"{key} = {value}\n")


def load_settings():
    settings = {}
    try:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split("=")
                settings[key.strip()] = value.strip()
    except FileNotFoundError:
        # Создание файла settings.txt со стандартными настройками
        settings = {
            "sort_list": "sell_lp_profit",
            "lp_store_parser_number_view_items": "all",
#            "sort_list_counter_2_view": "0",
#            "filter_lp_number": "None",
            "filter_min_isk_per_lp": -20000,
            "market_region": "jita",
            "sales_tax": "0.05"
        }
        save_settings(settings)

    return settings

# Настройка интерфейса вывода информации
sort_list = "sell_lp_profit"                # Сортировака вывода товаров по sell ордерам ("sell_lp_profit") или ("buy_lp_profit")
#sort_list = "buy_lp_profit"                # Сортировака вывода товаров по buy ордерам
lp_store_parser_number_view_items = 'all'           # Указывать 'all' или число
sort_list_counter_2_view = 0
filter_lp_number = None

# Настройка региона
market_region = "jita"
sales_tax = 0.05                            # Изменение налога на продажу (например, 0.05 для 5%)


auto_time_update = 5                             # Настройка времени обновления информации
