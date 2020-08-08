import os
from dotenv import load_dotenv
from vkbottle import Bot, Message
from parsers.parserCinema import cinema
from vkbottle.api.keyboard import Keyboard, Text
from vkbottle.rule import AbstractRule
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
TOKEN = os.environ.get("SECRET_KEY")
bot = Bot(TOKEN)
buffer_name = {}
days = ['Сегодня', 'Завтра', 'Послезавтра']
day_num = 0
session_array = []
session_full = {}
name = []


# Клавиатуры
def keyboard_cinema(index):
    check = 0
    buffer = cinema(index)
    keyboard = Keyboard()
    keyboard.add_row()
    for buf in buffer:
        check += 1
        if check <= 2:
            keyboard.add_button(Text(buf['name']), color="positive")
        else:
            check = 1
            keyboard.add_row()
            keyboard.add_button(Text(buf['name']), color="positive")

    return keyboard.generate()


def keyboard(num):
    check = 0
    buffer_cinema = cinema(day_num)
    sessions = buffer_cinema[num]['sessions']
    keyboard = Keyboard()
    keyboard.add_row()
    for session in sessions:
        check += 1
        if check <= 2:
            keyboard.add_button(Text('{time}({price}, {format})'.format(time=session['time'], price=session['price'], format=session['format'])), color="positive")
        else:
            check = 1
            keyboard.add_row()
            keyboard.add_button(Text('{time}({price}, {format})'.format(time=session['time'], price=session['price'], format=session['format'])), color="positive")

    return keyboard.generate()


def day():
    keyboard = Keyboard()
    keyboard.add_row()
    keyboard.add_button(Text('Сегодня'), color="positive")
    keyboard.add_button(Text('Завтра'), color="positive")
    keyboard.add_row()
    keyboard.add_button(Text('Послезавтра'), color="positive")
    return keyboard.generate()


# Кастомные правила
class MovieCheck(AbstractRule):
    async def check(self, message: Message):
        global name
        if len(name) != 0 and (message.text in name):
            return True


class SessionCheck(AbstractRule):
    async def check(self, message: Message):
        global session_array
        if len(session_array) != 0 and (message.text in session_array):
            return True


# Все запросы
@bot.on.message(text="начать", lower=True)
async def begin(ans: Message):
    await ans("Выберите день", keyboard=day())


@bot.on.message(text=days, lower=True)
async def choose_film(ans: Message):
    global day_num
    day_num = days.index(ans.text)
    buffer_cinema = cinema(day_num)
    await ans("Выберите фильм", keyboard=keyboard_cinema(day_num))
    for num, buf in enumerate(buffer_cinema, start=0):
        buffer_name.update(
            {buf['name']: num}
        )
        name.append(buf['name'])


@bot.on.message(MovieCheck())
async def choose_session(ans: Message):
    global session_array
    buffer_cinema = cinema(day_num)
    await ans("Выберите время сеанса", keyboard=keyboard(buffer_name[str(ans.text)]))
    for i, buf in enumerate(buffer_cinema, start=0):
        sessions = buf['sessions']
        for j, session in enumerate(sessions, start=0):
            ses = '{time}({price}, {format})'.format(time=session['time'], price=session['price'], format=session['format'])
            session_array.append(ses)
            session_full.update(
                {ses: i}
            )


@bot.on.message(SessionCheck())
async def full_info(ans: Message):
    await ans("Спасибо, что воспользовались нашим сервисом. Приятного вам просмотра")
    buffer_cinema = cinema(day_num)
    num = session_full[ans.text]
    href = buffer_cinema[num]['href']
    return href
bot.run_polling()