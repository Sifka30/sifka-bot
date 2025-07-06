import telebot
import schedule
import time
import threading

# 🔑 Вставь сюда свой токен
API_TOKEN = '7951673327:AAFTj5v_thFiBSAkYWlUi3Wq6TMVAp_CmKE'

bot = telebot.TeleBot(API_TOKEN)

# ID чата — пока один пользователь. Введи свой user_id (временно можно сделать так, чтобы бот сам тебе писал)
user_ids = [ ]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id not in user_ids:
        user_ids.append(message.chat.id)
    bot.send_message(message.chat.id, "👋 Доброе утро, @sifka1!\nТвои криптосигналы будут приходить каждый день в 08:30 по Софии 🇧🇬")

def send_daily_message():
    for uid in user_ids:
        bot.send_message(uid, "📈 Утренний криптосигнал:\nBTC: $109,000\nETH: $6,200\n(примерные данные)")

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Планируем рассылку
schedule.every().day.at("05:30").do(send_daily_message)  # 05:30 UTC = 08:30 София

# Запускаем планировщик в отдельном потоке
threading.Thread(target=schedule_checker).start()

print("🤖 Бот запущен...")
bot.infinity_polling()
