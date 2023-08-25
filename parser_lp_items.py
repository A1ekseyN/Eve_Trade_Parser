from bs4 import BeautifulSoup
import requests
import time


# State Protectorate - Caldati Navy +
# Federal Defence Union - Gallente +
# 24th Imperial Crusade - Amarr +
# Tribal Liberation Force - Minmatar +

# Outer Ring Excavations - ORE


start_time = time.time()
work_time = 0

base_url = "https://www.ellatha.com/eve/LPIndex-"

page_index = 1
#page_index = 101
#last_page_index = 101
last_page_index = 31661

pages_total_cnt = (last_page_index - page_index) // 20


faction = 'Outer Ring Excavations'
items_list = []

print(f"Start Parsing - {faction}")

while page_index <= last_page_index:
    time_for = time.time()

    if (page_index - 1) % 2000 == 0 and page_index != 1:
        for item in items_list:
            print(item)
        print()

    try:
        url = f"{base_url}{page_index}"
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data_rows = soup.select('table.box tr[bgcolor="#F5F5F5"], table.box tr[bgcolor="#FFFFFF"]')

        for row in data_rows:
            columns = row.find_all('td')
            faction_corp_name = columns[0].a.text.strip()
            if faction_corp_name == faction:
                reward_name = columns[2].text.strip()
                try:
                    lp_cost = int(columns[3].text.replace(',', '').strip())
                except ValueError:
                    lp_cost = None
                try:
                    isk_cost = int(columns[4].text.replace(',', '').strip())
                except ValueError:
                    isk_cost = None

                required_items_cell = columns[5]
                required_items_links = required_items_cell.find_all('a')
                required_items = [link.text for link in required_items_links]

                item_data = {
                    "item_name": reward_name,
                    "lp_store_components": {},
                    "lp_price": lp_cost,
                    "isk_price": isk_cost,
                    "quantity": 1,
                    "id": 0,
                }

                for required_item in required_items:
                    component_name, component_quantity = required_item.split(' x ')
                    item_data["lp_store_components"][component_name] = int(component_quantity)

                items_list.append(item_data)

        completion_percentage = (page_index / last_page_index) * 100
        time_cycle = time.time() - time_for
        work_time += time_cycle
        work_time_avg = work_time / (page_index / 20)

        print(f'- Items: {page_index}, Next: {page_index + 20}. Найдено: {len(items_list)} ({completion_percentage:.2f}%) '
              f'({time.time() - time_for:,.2f} sec) :: (avg: {work_time_avg:,.2f} sec)')

        page_index += 20
        time.sleep(0.1)

    except TimeoutError as error:
        print(f"!!! Произошла ошибка TimeoutError. Ожидание 10 секунд... ({time.time() - time_for:,.2f} sec)")
        print(f"Error: {error}")
        time.sleep(10)
        work_time += time_cycle
        continue
    except Exception as error:
        work_time += time_cycle
        print(f'ERROR: {error}')

print('+++')
for item in items_list:
    print(item)

print(f'\nTime: {(time.time() - start_time) // 60} minites')
