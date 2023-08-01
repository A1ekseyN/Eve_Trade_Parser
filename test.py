import requests

def get_access_token():
    # Здесь должен быть код для получения access token
    # Обычно это включает запрос на авторизацию и обмен временного кода на токен доступа
    access_token = "YOUR_ACCESS_TOKEN"
    return access_token

def get_character_balance(character_id, access_token):
    url = f"https://esi.evetech.net/latest/characters/{character_id}/wallet/"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        balance_data = response.json()
        total_balance = sum(entry["balance"] for entry in balance_data)
        return total_balance
    else:
        print("Ошибка при получении баланса персонажа")
        return None

def main():
    character_id = "YOUR_CHARACTER_ID"
    access_token = get_access_token()

    if access_token:
        total_balance = get_character_balance(character_id, access_token)
        print(f"Общий баланс ISK на персонаже: {total_balance:,.2f} ISK")

if __name__ == "__main__":
    main()
