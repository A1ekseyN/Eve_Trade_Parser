import requests
import time

from items_faction_wars import items_faction_wars_state_protectorate, items_component


start_time = time.time()

#items_faction_wars_state_protectorate = list(items_faction_wars_state_protectorate)

items = items_faction_wars_state_protectorate + items_component
items_prices_parsed = []
items_quantity = []


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
                        print(f"\nТовар: '{item_name}' в регионе '{region_name}' на станции '{station_name}':")

                        min_sell_price = station_prices["min_sell_price"]
                        max_buy_price = station_prices["max_buy_price"]
                        trade_volume = station_prices["trade_volume"]
                        profit_sell = station_prices["profit_sell"]
                        profit_sell_percentage = station_prices["profit_sell_percentage"]

                        print(f"Sell Price: {min_sell_price:,.0f}, Buy Price: {max_buy_price:,.0f}")
                        print(f"Торговый объем - {trade_volume:,.0f} items")
                        print(f"Profit: {profit_sell:,.2f} isk - {profit_sell_percentage:.2f}%")
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


# Калькулятор цен
#for item in items_prices_parsed:
#    print(item)


# Калькулятор себестоимости обмена LP на предмет
print('\nComponents')
#for item in items_component:                                # Тут не понятно. Вроде работает, но возможно нужно добавить еще один цикл
total_price = 0
for j in items_faction_wars_state_protectorate:
    print(f'Item: {j["item_name"]}')
    for component, quantity in j["lp_store_components"].items():
#        print('Check')
#        print(quantity)
        for price in items_prices_parsed:
            if component == price[60003760]["item_name"]:
                print(f'Component {component} - Price: {price[60003760]["min_sell_price"]}')
                total_price += price[60003760]["min_sell_price"] * quantity
    total_price += j["isk_price"]       # Добавляем стоимость в isk
    isk_price = j["isk_price"]
#       print(isk_price)
#       items_quantity.extend([j["item_name"], total_price])
    items_quantity.append({"item_name": j["item_name"], "total_price": total_price})
    total_price = 0

    print('!!!!!!!')
    print(items_quantity)



#            print(total_price)
#            print(j["isk_price"])
#            total_price += 0

#                    print(component)
#                    print(price[60003760]["item_name"])
#                    print(price[60003760]["min_sell_price"])
    print(f'Item: {j["item_name"]}, Cost Price: {total_price:,.0f} isk (ISK: {j["isk_price"]:,.0f} + LP ()) // Buy Income:  // Sell Income: ')


#print(items_quantity)
#print(items_quantity[0]["total_price"])

print('\n+++ Items +++')

# Вывод информации о ценах
cnt = 0
#print(len(items_quantity))

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
                        item_buy_price = j_parsed[60003760]["max_buy_price"] * item["quantity"]
                        item_total_price = items_quantity[cnt]["total_price"]
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

                        print(f'\n{item["item_name"]} - Buy: {j_parsed[60003760]["max_buy_price"]:,.0f} isk // Sell: {j_parsed[60003760]["min_sell_price"]:,.0f} isk // Buy Profit: {((j_parsed[60003760]["max_buy_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]):,.0f} isk // Sell Profit: {(j_parsed[60003760]["min_sell_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]:,.2f} isk // \nBuy LP Profit: {((j_parsed[60003760]["max_buy_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]:,.0f} lp-isk // Sell LP Profit: {((j_parsed[60003760]["min_sell_price"]  * item["quantity"]) - items_quantity[cnt]["total_price"]) // item["lp_price"]:,.0f} lp-isk ')
                        cnt += 1



print('\nPass')
print(f'\nTime: {time.time() - start_time} sec')

#print(items_prices_parsed)
