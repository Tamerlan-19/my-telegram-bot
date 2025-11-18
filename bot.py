import telebot
import re
import traceback

TOKEN = "7608592669:AAGs1SbO-HoUjwzEtjSAwofU7KI5fA6JrNY"
ADMIN_CHAT_ID = 6064393014

bot = telebot.TeleBot(TOKEN)

# ====== Декоратор для обработки ошибок ======
def admin_error_handler(func):
    def wrapper(message):
        try:
            func(message)
        except Exception as e:
            error_text = f"⚠️ Ошибка в боте:\n{e}\n\n{traceback.format_exc()}"
            try:
                bot.send_message(ADMIN_CHAT_ID, error_text)
            except:
                print("Не удалось отправить сообщение админу:", error_text)
    return wrapper

# ====== Команда /createbutton ======
@bot.message_handler(commands=['createbutton'])
@admin_error_handler
def create_button(message):
    pattern = r'/createbutton\s+(\S+)\s+"(.+)"\s+"(.+)"'
    match = re.match(pattern, message.text)

    if not match:
        bot.reply_to(
            message,
            '❗ Использование:\n'
            '/createbutton URL "Текст кнопки" "Текст сообщения"'
        )
        return

    url = match.group(1)
    button_text = match.group(2)
    post_text = match.group(3)

    if message.chat.type != "channel":
        bot.reply_to(message, "❗ Команду можно использовать только в канале, где бот является администратором.")
        return

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(button_text, url=url))

    bot.send_message(message.chat.id, post_text, reply_markup=markup)

# ====== Команда /checkstatus ======
@bot.message_handler(commands=['checkstatus'])
@admin_error_handler
def check_status(message):
    bot.reply_to(message, "Works well ✅")

# ====== Отправка сообщения при старте ======
def notify_startup():
    try:
        bot.send_message(ADMIN_CHAT_ID, "Bot live 🟢")
    except Exception as e:
        print(f"Не удалось отправить стартовое сообщение: {e}")

# ====== Старт бота ======
if __name__ == "__main__":
    notify_startup()
    bot.infinity_polling()

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        bot.send_message(ADMIN_CHAT_ID, f"Server down ⛔ Error:\n{e}")
