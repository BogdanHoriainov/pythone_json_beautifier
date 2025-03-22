from telebot import TeleBot, types
import json
import random

bot = TeleBot(token='YOUR_API_TOKEN', parse_mode='html') 

# создаем кнопки
def create_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🌐 Визитка")
    item2 = types.KeyboardButton("📨 Написать автору")
    item3 = types.KeyboardButton("🚀 Код проекта")
    item4 = types.KeyboardButton("🎲 Генерировать тестовый JSON")
    markup.add(item1, item2, item3, item4)
    return markup

# ответ на /start
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    markup = create_markup()
    bot.send_message(
        chat_id=message.chat.id,
        text='Привет! Я помогу проверить твой JSON и оформить его в удобный для чтения вид. Отправь JSON-строку, и я разберу её для тебя. Также ты можешь сгенерировать JSON:',
        reply_markup=markup
    )

# обработчик JSON
@bot.message_handler(func=lambda message: is_json(message.text))
def json_handler(message: types.Message):
    markup = create_markup() 
    payload = json.loads(message.text)
    formatted_text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'JSON:\n<code>{formatted_text}</code>',
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def message_handler(message: types.Message):
    markup = create_markup()
    if message.chat.type == 'private':
        if message.text == '🌐 Визитка':
            bot.send_message(message.chat.id, 'На стадии разработки, скоро будет готово!🛠️🔥', reply_markup=markup)
        elif message.text == '🚀 Код проекта':
            bot.send_message(message.chat.id, 'https://github.com/BogdanHoriainov/pythone_json_beautifier', reply_markup=markup)
        elif message.text == '📨 Написать автору':
            bot.send_message(message.chat.id, 'https://t.me/chifuyu_cf', reply_markup=markup)
        elif message.text == '🎲 Генерировать тестовый JSON': 
            test_json = generate_random_json() 
            bot.send_message(message.chat.id, f'JSON:\n<code>{test_json}</code>', reply_markup=markup)
        else:
            # пытаемся распарсить JSON    
            try:
                payload = json.loads(message.text)
                formatted_text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'JSON:\n<code>{formatted_text}</code>',
                    reply_markup=markup
                )
            except json.JSONDecodeError as ex:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'При обработке произошла ошибка:\n<code>{str(ex)}</code>',
                    reply_markup=markup
                )

# Генерируем случайный JSON
def generate_random_json():
    random_data = {
        "name": random.choice(["Alice", "정민", "Charlie", "Cat"]),
        "age": random.randint(18, 40),
        "city": random.choice(["New York", "London", "Seoul", "Tokyo"]),
        "email": f"{random.choice(['alice', 'jeongmin', 'charlie', 'cat'])}@example.com"
    }
    return json.dumps(random_data, indent=2, ensure_ascii=False)

# Проверяем, является ли строка корректным JSON
def is_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()
