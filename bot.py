import telebot
import requests
import csv
from io import StringIO
import os

TOKEN = os.getenv("8513122207:AAGBgK3PrNtRKv3TpeegHBkS3BnsU3pJTow")
SHEET_CSV_URL = os.getenv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTzFU40Gy6ZUNSDnv_uCQsqvAGnHDM9TcGr1NFpQopB8qSHMnGgrY63WjsZU5e_7yJFO4NZ3hsyjWOr/pub?output=csv")

bot = telebot.TeleBot(TOKEN)

def ambil_data_sheet():
    response = requests.get(SHEET_CSV_URL)
    f = StringIO(response.text)
    reader = csv.DictReader(f)
    return list(reader)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Ketik:\n/search kata kunci")

@bot.message_handler(commands=['search'])
def cari(message):
    query = message.text.replace('/search ', '').lower()
    data = ambil_data_sheet()

    hasil = []
    for item in data:
        if query in item['nama'].lower() or query in item['deskripsi'].lower():
            hasil.append(item)

    if not hasil:
        bot.reply_to(message, "Data tidak ditemukan.")
        return

    for item in hasil:
        teks = f"""
<b>{item['nama']}</b>
Harga: Rp{item['harga']}
{item['deskripsi']}
<a href="{item['link']}">Buka Link</a>
"""
        bot.send_message(message.chat.id, teks, parse_mode="HTML")

bot.infinity_polling()
