from vkbottle.bot import Blueprint, Message
from parsers.parserCinema import cinema, get_theater
from vkbottle.api.keyboard import Keyboard, Text
from vkbottle.rule import AbstractRule
from botDB import information, check_person, get_city, update_city
from anything.translit import transliterate
bp = Blueprint(name="Синема Парк")


# Переменные для разработки
buffer_name = {}
days = ['Сегодня', 'Завтра', 'Послезавтра']
cities = ['Москва', 'Санкт-Петербург', 'Белгород', 'Волгоград', 'Вологда', 'Воронеж', 'Екатеринбург',
        'Ижевск', 'Калининград', 'Ковров', 'Краснодар', 'Красноярск', 'Мурманск', 'Набережные Челны',
        'Нижний Новгород', 'Новокузнецк', 'Новосибирск', 'Пермь', 'Рязань', 'Самара', 'Саратов',
        'Сочи', 'Ставрополь', 'Сургут', 'Сыктывкар', 'Тула', 'Тюмень', 'Ульяновск', 'Уфа', 'Челябинск'
        ]
theater_url = {
    'Белгород': 'belgorodskiy/', 'Волгоград': 'evropa-city-mall/', 'Вологда': 'marmelad/',
    'Екатеринбург': 'alatyr/','Ижевск': 'petrovskiy/', 'Калининград': 'evropa/', 'Ковров': 'kovrov-mall/',
    'Краснодар': 'oz/', 'Красноярск': 'galeraya-enisey/', 'Мурманск': 'forum/', 'Набережные Челны': 'torgoviy-kvartal/',
    'Новокузнецк': 'imax/', 'Рязань': 'viktoria-plaza/', 'Самара': 'park-haus/','Сочи': 'more-moll/', 'Ставрополь': 'kosmos/',
    'Сургут': 'surgut-city-mall/', 'Сыктывкар': 'maxi/', 'Тула': 'maxi/', 'Тюмень': 'gudvin/', 'Ульяновск': 'akvamoll/',
    'Челябинск': 'gorki/'
}
day_num = 0
session_array = []
session_full = {}
name = []
recent_actions = []


# Клавиатуры
def keyboard_main():
    keyboard = Keyboard()
    keyboard.add_row()
    keyboard.add_button(Text('Изменить геолокацию'), color="secondary")
    keyboard.add_button(Text('Кино'), color="positive")
    return keyboard.generate()


def keyboard_cinema(index, URL):
    check = 0
    buffer = cinema(index, URL)
    if len(buffer) != 0:
        keyboard = Keyboard()
        keyboard.add_row()
        for buf in buffer:
            check += 1
            if check <= 3:
                keyboard.add_button(Text(buf['name']), color="positive")
            else:
                check = 1
                keyboard.add_row()
                keyboard.add_button(Text(buf['name']), color="positive")
        keyboard.add_row()
        keyboard.add_button(Text('Назад'), color="secondary")
        return keyboard.generate()

    else:
        return 'В данный момент доступных сеансов нет'


def keyboard_ses(num, URL):
    check = 0
    buffer_cinema = cinema(day_num, URL)
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


def keyboard_day():
    keyboard = Keyboard()
    keyboard.add_row()
    keyboard.add_button(Text('Сегодня'), color="positive")
    keyboard.add_button(Text('Завтра'), color="positive")
    keyboard.add_row()
    keyboard.add_button(Text('Послезавтра'), color="positive")
    return keyboard.generate()


def keyboard_city(from_, before):
    check = 0
    keyboard = Keyboard(inline=True)
    keyboard.add_row()
    for i in range(from_, before):
        check += 1
        if check <= 2:
            keyboard.add_button(Text(cities[i]), color="positive")
        else:
            check = 1
            keyboard.add_row()
            keyboard.add_button(Text(cities[i]), color="positive")
    return keyboard.generate()


def keyboard_theater():
    check = 0
    keyboard = Keyboard()
    keyboard.add_row()
    print(response_name)
    print(len(response_name))
    for (num, response) in enumerate(response_name):
        if num > 17:
            break
        else:
            check += 1
            if len(response) >= 40:
                response = response[0: 39]
            if check <= 2:
                keyboard.add_button(Text(response), color="positive")
            else:
                check = 1
                keyboard.add_row()
                keyboard.add_button(Text(response), color="positive")
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


class TheaterCheck(AbstractRule):
    async def check(self, message: Message):
        if len(response_name) and message.text in response_name:
            return True


# message запросы
@bp.on.message(text="начать", lower=True)
async def begin(ans: Message):
    check_user = check_person(ans.from_id)
    if check_user == 1:
        await ans('Вы находитесь в главном меню'
                  , keyboard=keyboard_main())
    else:
        await ans('Выберите город, в котором вы находитесь', keyboard=keyboard_city(0, 10))
        await ans('Выберите город, в котором вы находитесь', keyboard=keyboard_city(11, 21))
        await ans('Выберите город, в котором вы находитесь', keyboard=keyboard_city(20, 29))


@bp.on.message(text=cities, lower=True)
async def choose(ans: Message):
    information(ans.from_id, ans.text)
    await ans('Ваши настройки сохранены. \
              Нажмте кнопку «Кино», чтобы продолжить.', keyboard=keyboard_main())


@bp.on.message(text=days, lower=True)
async def choose_film(ans: Message):
    global day_num
    day_num = days.index(ans.text)
    buffer_cinema = cinema(day_num, URL)
    await ans("Выберите фильм", keyboard=keyboard_cinema(day_num, URL))
    for num, buf in enumerate(buffer_cinema, start=0):
        buffer_name.update(
            {buf['name']: num}
        )
        name.append(buf['name'])
    recent_actions.append(ans.text)


@bp.on.message(MovieCheck())
async def choose_session(ans: Message):
    global session_array
    buffer_cinema = cinema(day_num, URL)
    await ans("Выберите время сеанса", keyboard=keyboard_ses(buffer_name[str(ans.text)], URL))
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
    buffer_cinema = cinema(day_num, URL)
    num = session_full[ans.text]
    href = buffer_cinema[num]['href']
    if recent_actions[-1] in session_array:
        pass
    else:
        recent_actions.append(ans.text)
    return href


@bp.on.message(text="Кино", lower=True)
async def movie(ans: Message):
    global URL
    global response_name
    global dict_theater
    response_name = []
    dict_theater = {}
    response = get_theater(transliterate(get_city(ans.from_id)))
    for res in response:
        response_name.append(res['name'])
        dict_theater.update(
            {
                res['name']: res['href']
             }
                            )
    if len(response) == 0:
        URL = 'https://kinoteatr.ru/raspisanie-kinoteatrov/' + transliterate(get_city(ans.from_id)) +'/' + theater_url[get_city(ans.from_id)]
        await ans("Выберите день", keyboard=keyboard_day())
    else:
        await ans("Выберите интересующий кинотеатр", keyboard=keyboard_theater())


@bp.on.message(text="Изменить геолокацию", lower=True)
async def geometa(ans: Message):
    await ans('Выберите город, в котором вы находитесь', keyboard=keyboard_city(0, 10))
    await ans('Выберите город, в котором вы находитесь', keyboard=keyboard_city(11, 21))
    await ans('Выберите город, в котором вы находитесь', keyboard=keyboard_city(20, 29))


@bp.on.message(TheaterCheck())
async def theater(ans: Message):
    global URL
    URL = dict_theater[ans.text]
    await ans('Выберите день', keyboard=keyboard_day())


@bp.on.message(text="Назад", lower=True)
async def back(ans: Message):
    if recent_actions[-1] in session_array:
        await ans('Выберите фильм', keyboard=keyboard_cinema(day_num, URL))
        recent_actions.pop(-1)
    elif recent_actions[-1] in name:
        await ans('Выберите фильм', keyboard=keyboard_cinema(day_num, URL))
        recent_actions.pop(-1)
    elif recent_actions[-1] in days:
        await ans('Выберите день', keyboard=keyboard_day())
        recent_actions.pop(-1)
    print(recent_actions)
