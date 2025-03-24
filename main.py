import json
import random
import re
from telebot import TeleBot, types

bot = TeleBot("YOUR_API_TOKEN")



def create_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("🌐 Визитка"),
        types.KeyboardButton("📨 Написать автору"),
        types.KeyboardButton("🚀 Код проекта"),
        types.KeyboardButton("🎭 Генерировать тестовый JSON")
    )
    return markup

@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Привет! Я помогу проверить твой JSON и оформить его в удобный для чтения вид. Отправь JSON-строку, и я разберу её для тебя. Также ты можешь сгенерировать JSON:',
        reply_markup=create_markup()
    )

@bot.message_handler(content_types=['text'])
def message_handler(message: types.Message):
    text = message.text.strip()
    markup = create_markup()
    
    if text == '🌐 Визитка':
        bot.send_message(message.chat.id, 'На стадии разработки, скоро будет готово!🛠🔥', reply_markup=markup)
    elif text == '🚀 Код проекта':
        bot.send_message(message.chat.id, 'https://github.com/BogdanHoriainov/pythone_json_beautifier', reply_markup=markup)
    elif text == '📨 Написать автору':
        bot.send_message(message.chat.id, 'https://t.me/chifuyu_cf', reply_markup=markup)
    elif text == '🎭 Генерировать тестовый JSON':
        bot.send_message(message.chat.id, f'JSON:\n<code>{generate_random_json()}</code>', reply_markup=markup, parse_mode='HTML')
    else:
        # исправляем JSON
        fixed_json = fix_json(text)
        if fixed_json:
            bot.send_message(message.chat.id, f'Исправленный JSON:\n<code>{fixed_json}</code>', reply_markup=markup, parse_mode='HTML')
        else:
            # пытаемся распарсить
            try:
                payload = json.loads(text)
                formatted_json = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
                bot.send_message(message.chat.id, f'JSON:\n<code>{formatted_json}</code>', reply_markup=markup, parse_mode='HTML')
            except json.JSONDecodeError as ex:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'При обработке произошла ошибка:\n<code>{str(ex)}</code>',
                    parse_mode='HTML'
                )

def fix_json(text):
    try:
        text = text.strip()
        if not text.startswith("{"):
            text = "{" + text
        if not text.endswith("}"):
            text += "}"
        payload = json.loads(text)
        return json.dumps(payload, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return None

def generate_random_json():
    return json.dumps({
        "name": random.choice(["Alice", "정민", "Charlie", "Cat"]),
        "age": random.randint(18, 40),
        "city": random.choice(["New York", "London", "Seoul", "Tokyo"]),
        "email": f"{random.choice(['alice', 'jeongmin', 'charlie', 'cat'])}@example.com"
    }, indent=2, ensure_ascii=False)

def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()
