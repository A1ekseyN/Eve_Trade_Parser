from lp_store_items_state_protectorate import *
from lp_store_items_sisters_of_eve import *
from lp_store_items_outer_ring_excavations import *


version = "0.0.1d"
DEBUG_MODE = False
colors = True    # Включает и выключает цветовую индикацию. Цвета нужно выключать, когда программа компилируется в *.exe


settings = {"lp_faction": "state_protectorate",
#            "lp_faction": "sisters_of_eve",
#            "lp_faction": "outer_ring_excavations",
            "sort_list": "sell_lp_profit",
            "lp_store_parser_number_view_items": "all",
#            "sort_list_counter_2_view": "0",
#            "filter_lp_number": "None",
            "filter_min_isk_per_lp": -200000,
            "market_region": "jita",
            "sales_tax": 0.05,
            }


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
            "lp_faction": "state_protectorate",
            "sort_list": "sell_lp_profit",
            "lp_store_parser_number_view_items": "all",
#            "sort_list_counter_2_view": "0",
#            "filter_lp_number": "None",
            "filter_min_isk_per_lp": -20000,
            "market_region": "jita",
            "sales_tax": 0.05
        }
        save_settings(settings)

    return settings

# Настройка интерфейса вывода информации
sort_list = "sell_lp_profit"                # Сортировака вывода товаров по sell ордерам ("sell_lp_profit") или ("buy_lp_profit")
#sort_list = "buy_lp_profit"                # Сортировака вывода товаров по buy ордерам
lp_store_parser_number_view_items = 'all'           # Указывать 'all' или число
sort_list_counter_2_view = 0
filter_lp_number = None
auto_time_update = 5                             # Настройка времени обновления информации


# Настройка региона
#lp_faction = settings["lp_faction"]
market_region = settings["market_region"]                      # jita, amarr, hek, rens
sales_tax = settings["sales_tax"]                              # Изменение налога на продажу (например, 0.05 для 5%)

# Настройка Фракции, которую ищем


# Выбор market region
if market_region == 'jita':
    regions = [{"id": 10000002, "name": "The Forge"}]
    stations = [{"id": 60003760, "name": "Jita 4-4 - Caldari Navy Assembly Plant"}]
elif market_region == 'amarr':
    regions = [{"id": 10000043, "name": "Domain"}]
    stations = [{"id": 60008494, "name": "Amarr VIII (Oris) - Emperor Family Academy"}]
elif market_region == 'dodixie':
    regions = [{"id": 10000032, "name": "Sinq Laison"}]
    stations = [{"id": 60011866, "name": "Dodixie IX - Moon 20 - Federation Navy Assembly Plant"}]
elif market_region == 'hek':
    regions = [{"id": 10000042, "name": "Metropolis"}]
    stations = [{"id": 60005686, "name": "Hek VIII - Moon 12 - Boundless Creation Factory"}]
elif market_region == 'rens':
    regions = [{"id": 10000030, "name": "Heimatar"}]
    stations = [{"id": 60004588, "name": "Rens VI - Moon 8 - Brutor Tribe Treasury"}]


# Настройка Фракции.
# Сюда нужно добавить items, которые собираются в зависимости от фракции
if settings['lp_faction'] == "state_protectorate":
#    lp_faction = "state_protectorate"
    items_component_settings = items_component_state_protectorate + items_faction_wars_state_protectorate
    items_in_lp_store = items_faction_wars_state_protectorate
elif settings['lp_faction'] == "sisters_of_eve":
#    lp_faction = "sisters_of_eve"
    items_component_settings = items_component_sisters_of_eve + items_in_lp_store_sisters_of_eve
    items_in_lp_store = items_in_lp_store_sisters_of_eve
elif settings['lp_faction'] == "outer_ring_excavations":
    items_component_settings = items_component_outer_ring_excavations + items_in_lp_store_ore_outer_ring_excavations
    items_in_lp_store = items_in_lp_store_ore_outer_ring_excavations


def change_lp_store(ask_lp_store):
    if ask_lp_store == 1:
#        lp_faction = "state_protectorate"
        settings["lp_faction"] = "state_protectorate"
        items_component_settings = items_component_state_protectorate + items_faction_wars_state_protectorate
        items_in_lp_store = items_faction_wars_state_protectorate
        print('Change LP Store')
        save_settings(settings)
        return items_component_settings, items_in_lp_store, settings

    elif settings['lp_faction'] == "sisters_of_eve":
    #    lp_faction = "sisters_of_eve"
        items_component_settings = items_component_sisters_of_eve + items_in_lp_store_sisters_of_eve
        items_in_lp_store = items_in_lp_store_sisters_of_eve
    return items_component_settings, items_in_lp_store

