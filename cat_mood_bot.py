import config

from os import listdir, path
from telebot import TeleBot, types
from random import choice, randint

TRIGGER = ('зюсь', 'зол', 'злой', 'злющий', 'раздражен', 'печаль', 'отчаяние', 'безысходность', 'гнев', 'кайф',
           'зашибись', 'заебись', 'отстой', 'котик', 'печальный', 'гневе', 'бесит', 'бесят', 'хмурюсь', 'кайфую',
           'весело', 'весел', 'хмур', 'весеюсь', 'глусно', 'бешусь', 'кот', 'учаня', 'учань')

random_chanse = {}

bot = TeleBot(token=config.TOKEN, parse_mode='html')

card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
card_type_keybaord.row(
    types.KeyboardButton(text='😾 Зюсь'),
    types.KeyboardButton(text='😸 Весеюсь'),
    types.KeyboardButton(text='😿 Глусно')
)


def send_photo(message: types.Message):
    images = path.join('img', choice(listdir('img')))
    bot.send_photo(message.chat.id, photo=open(images, 'rb'))


@bot.message_handler(commands=['/setrandom'])
def start_command_handler(message: types.Message):
    if len(message.text.split()) > 1 and message.text.split()[1].isdigit() and len(message.text.split()[1]) < 4:
        random_chanse[str(message.chat.id)] = int(message.text.split()[1])
        bot.send_message(
            chat_id=message.chat.id,
            text=f'установлен шанс срабатывания триггера {random_chanse[str(message.chat.id)]}%',
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='После команды должна быть цифра от 0 до 100',
            reply_markup=card_type_keybaord,
        )


@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Этот бот отправляет котомемы \nМожно добавить в групповой чат'
             '\nДля частоты срабатывания триггера используй команду:'
             '\n/setrandom 0-100 (шанс срабатывания триггера)',
        reply_markup=card_type_keybaord,
    )


@bot.message_handler()
def message_handler(message: types.Message):
    if message.text in ('😾 Зюсь', '😸 Весеюсь', '😿 Глусно'):
        send_photo(message)
    elif any(i.lower() in TRIGGER for i in message.text.split()):
        chanse = 100
        if str(message.chat.id) in random_chanse:
            chanse = random_chanse[str(message.chat.id)]
        if randint(0, 100) <= chanse:
            send_photo(message)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
