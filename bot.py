import telebot
import requests
import schedule
import time
import threading
import datetime
import openai

# 🔐 OpenAI API ключ
openai.api_key = "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"

# 🔐 Telegram токен
bot = telebot.TeleBot("7951673327:AAFTj5v_thFiBSAkYWlUi3Wq6TMVAp_CmKE")

# 📊 Получение данных с CoinGecko
def get_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    r = requests.get(url)
    try:
        return r.json()[symbol]['usd']
    except:
        return "n/a"

def format_market_summary():
    coins = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'solana': 'SOL',
        'binancecoin': 'BNB',
        'ripple': 'XRP',
        'cardano': 'ADA'
    }
    msg = "📊 *Крипторынок на {}:*\n".format(datetime.datetime.now().strftime('%d.%m.%Y'))
    for key, label in coins.items():
        price = get_price(key)
        msg += f"{label}: ${price}\n"
    return msg

# 📬 Команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я криптобот 🤖\nОтправь /btc, /eth, /alts или задай любой вопрос!")

@bot.message_handler(commands=['btc'])
def btc_price(message):
    price = get_price('bitcoin')
    bot.reply_to(message, f"BTC: ${price}")

@bot.message_handler(commands=['eth'])
def eth_price(message):
    price = get_price('ethereum')
    bot.reply_to(message, f"ETH: ${price}")

@bot.message_handler(commands=['alts'])
def alts_price(message):
    summary = format_market_summary()
    bot.reply_to(message, summary, parse_mode='Markdown')

# 🤖 GPT-ответы
@bot.message_handler(func=lambda message: True)
def gpt_reply(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты дружелюбный криптопомощник, который отвечает просто и по делу."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "Ошибка при обращении к GPT: " + str(e))

# ⏰ Утренняя рассылка в 08:30 (по времени сервера)
def schedule_task():
    summary = format_market_summary()
    chat_id = '@sifka_channel'  # или ID группы/пользователя
    bot.send_message(chat_id, summary, parse_mode='Markdown')

def run_schedule():
    schedule.every().day.at("08:30").do(schedule_task)
    while True:
        schedule.run_pending()
        time.sleep(10)

threading.Thread(target=run_schedule).start()

print("Бот запущен...")
bot.infinity_polling()
