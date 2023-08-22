from items_faction_wars import items_component, items_faction_wars_state_protectorate
from items_all_market import items_eve

items_component = items_component + items_faction_wars_state_protectorate
items_eve = items_eve


# Проверка соответствия id items во ФВ.
for component in items_component:
    match = False

    for item in items_eve:
        for i in items_component:
            if component["item_name"] == item["name"] and component["id"] == item["id"]:
                match = True
                break

    if match:
        pass
#        print("ok")
    else:
        print(f"Fail - {item['name']}")