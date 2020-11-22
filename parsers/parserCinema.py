import requests
from bs4 import BeautifulSoup as bS
import time
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def get_agent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    # Получить случайную строку пользовательского агента.
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent


headers = {
    'accept': '*/*',
    'user-agent': get_agent()
}


def type_time(v):
    return time.strftime(v)


def get_html(url):
    r = requests.get(url, headers=headers).text
    return r


def get_content_cinema(html):
    soup = bS(html, 'lxml')
    buf = []
    items = soup.find_all('div', class_="shedule_movie bordered gtm_movie")
    for item in items:
        infoSession = []
        infoSessionSearch = item.find_all('a', class_="shedule_session")
        for info in infoSessionSearch:
            time = info.find('span', class_="shedule_session_time").get_text(strip=True)
            price = info.find('span', class_="shedule_session_price").get_text(strip=True)
            format = info.find('span', class_="shedule_session_format").get_text(strip=True)
            infoSession.append(
                {
                    'time': time,
                    'price': price,
                    'format': format
                }
            )

        buf.append({
            'name': item.find('a').get('data-gtm-ec-name'),
            'href': item.find('a').get('href'),
            'sessions': infoSession
        })
    return buf


def get_theater(city):
    if city == 'Moskva':
        url = 'https://kinoteatr.ru/raspisanie-kinoteatrov/'
    else:
        url = 'https://kinoteatr.ru/raspisanie-kinoteatrov/{city}'.format(city=city)
    print(url)
    html = get_html(url)
    soup = bS(html, 'lxml')
    items = soup.find_all('div', class_="col-md-12 cinema_card")
    buf = []
    for item in items:
        buf.append(
            {
                'name':  item.find('div', class_='cinema_card_wrap_description').find('a').find('h3').get_text(strip=True),
                'href': item.find('div', class_='cinema_card_wrap_description').find('a').get('href')
            }
        )
    return buf


def cinema(numberDay, URL):
    day = int(type_time('%d')) + numberDay
    if day < 10:
        dayNormal = '0' + str(day)
    else:
        dayNormal = str(day)

    url = URL + '?date=' + type_time("%Y") + "-" + type_time("%m") + "-" + dayNormal
    html = get_html(url)
    return get_content_cinema(html)

