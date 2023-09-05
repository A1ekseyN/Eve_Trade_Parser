import telebot
from telebot import types
import json


bot = telebot.TeleBot('6273285286:AAFlrAn4Rl6FfMVusypufImuTANiSW_HmFQ')


# Загрузка данных из файла lp_state_protectorate.json
def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


@bot.message_handler(commands=['start', 'hello', '+'])
def main(message):
    bot.send_message(message.chat.id, 'Hello\n/ORE\n/state_protectorate')


@bot.message_handler(commands=['state_protectorate', 'state protectorate', 'stateprotectorate'])
def show_lp_store_state_protectorate(message):
    data = load_data('lp_state_protectorate.json')
    state_protectorate = ""

    for item in data[:20]:
        state_protectorate += f"<b>{item['item_name']}:</b>\nBuy: {item['buy_lp_profit']} (Vol: {item['buy_volume']})\nSell: {item['sell_lp_profit']}\n\n"

    bot.send_message(message.chat.id, state_protectorate, parse_mode='HTML')


@bot.message_handler(commands=['ORE'])
def show_lp_store_ore_outer_ring_excavations(message):
    data = load_data('lp_state_protectorate.json')
    ore_data = ""

    for item in data[:20]:
        ore_data += f"<b>{item['item_name']}:</b>\nBuy LP Profit: {item['buy_lp_profit']} (Vol: {item['buy_volume']})\nSell LP Profit: {item['sell_lp_profit']}\n\n"

    bot.send_message(message.chat.id, ore_data, parse_mode='HTML')


bot.polling(none_stop=True)
