from vkbottle.bot import Blueprint, Message
from parsers.parserCinema import cinema
from vkbottle.api.keyboard import Keyboard, Text
from vkbottle.rule import AbstractRule
from botDB import information
bp = Blueprint(name="Синема Парк")
# Переменные для разработки
buffer_name = {}
days = ['Сегодня', 'Завтра', 'Послезавтра']
day_num = 0
session_array = []
session_full = {}
name = []
recent_actions = []


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
    keyboard.add_row()
    keyboard.add_button(Text('Назад'), color="secondary")
    return keyboard.generate()


def keyboard_ses(num):
    check = 0
    buffer_cinema = cinema(day_num)
    sessions = buffer_cinema[num]['sessions']
    keyboard = Keyboard()
    keyboard.add_row()
    for session in sessions:
        check += 1
        if check <= 2:
            keyboard.add_button(Text(
                '{time}({price}, {format})'.format(time=session['time'], price=session['price'],
                                                   format=session['format'])), color="positive")
        else:
            check = 1
            keyboard.add_row()
            keyboard.add_button(Text(
                '{time}({price}, {format})'.format(time=session['time'], price=session['price'],
                                                   format=session['format'])), color="positive")
    keyboard.add_row()
    keyboard.add_button(Text('Назад'), color="secondary")
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
        if len(name) and (message.text in name):
            return True


class SessionCheck(AbstractRule):
    async def check(self, message: Message):
        global session_array
        if len(session_array) and (message.text in session_array):
            return True
# message запросы
@bp.on.message(text="начать", lower=True)
async def begin(ans: Message):
    await ans("Выберите день", keyboard=day())
    return information(ans.from_id)


@bp.on.message(text=days, lower=True)
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

    recent_actions.append(ans.text)


@bp.on.message(MovieCheck())
async def choose_session(ans: Message):
    global session_array
    buffer_cinema = cinema(day_num)
    await ans("Выберите время сеанса", keyboard=keyboard_ses(buffer_name[str(ans.text)]))
    for i, buf in enumerate(buffer_cinema, start=0):
        sessions = buf['sessions']
        for j, session in enumerate(sessions, start=0):
            ses = '{time}({price}, {format})'.format(time=session['time'], price=session['price'], format=session['format'])
            session_array.append(ses)
            session_full.update(
                {ses: i}
            )
    if recent_actions[-1] in name:
        pass
    else:
        recent_actions.append(ans.text)


@bp.on.message(SessionCheck())
async def full_info(ans: Message):
    await ans("Спасибо, что воспользовались нашим сервисом. Приятного вам просмотра")
    buffer_cinema = cinema(day_num)
    num = session_full[ans.text]
    href = buffer_cinema[num]['href']
    if recent_actions[-1] in session_array:
        pass
    else:
        recent_actions.append(ans.text)
    return href


@bp.on.message(text="Назад", lower=True)
async def back(ans: Message):
    if recent_actions[-1] in session_array:
        await ans('Выберите фильм', keyboard=keyboard_cinema(day_num))
        recent_actions.pop(-1)
    elif recent_actions[-1] in name:
        await ans('Выберите фильм', keyboard=keyboard_cinema(day_num))
        recent_actions.pop(-1)
    elif recent_actions[-1] in days:
        await ans('Выберите день', keyboard=day())
        recent_actions.pop(-1)
    print(recent_actions)
