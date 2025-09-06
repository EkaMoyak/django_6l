import telebot
import requests
import json
from telebot import types

# Конфигурация
API_URL = 'http://127.0.0.1:8000/api/'
BOT_TOKEN = '8007601498:AAEFq1vQaGtpOdq27tLnYyjDcD_-hpySvzg'

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    """
    Обработчик команды /start
    Передает данные пользователя в Django API для регистрации
    """
    # Собираем полные данные пользователя
    user_data = {
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    try:
        # Отправляем POST запрос в Django API
        response = requests.post(
            API_URL + 'register/',  # Добавил слэш
            json=user_data,
            timeout=10  # Добавил таймаут
        )

        # Обрабатываем ответ от API
        if response.status_code in [200, 201]:
            try:
                result = response.json()
                if 'message' in result:
                    bot.reply_to(message, result['message'])
                else:
                    bot.reply_to(message, 'Вы успешно зарегистрированы!')
            except json.JSONDecodeError:
                bot.reply_to(message, 'Вы успешно зарегистрированы!')
        else:
            bot.reply_to(message, f'Ошибка регистрации. Код: {response.status_code}')

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, 'Произошла ошибка при подключении к серверу')
        print(f"Ошибка запроса: {e}")
    except Exception as e:
        bot.reply_to(message, 'Произошла неизвестная ошибка')
        print(f"Неизвестная ошибка: {e}")


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
Доступные команды:
/start - Регистрация в системе
/help - Показать помощь
"""
    bot.reply_to(message, help_text)


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)