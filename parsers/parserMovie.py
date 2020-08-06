import requests
from bs4 import BeautifulSoup as bS
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from anything.translit import transliterate


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


def get_html(url):
    r = requests.get(url, headers=headers).text
    return r


def movie_online(string):
    translit_string = transliterate(string)
    translit_string_full = translit_string.replace(' ', '-')
    URL = 'https://b7.x-film.top/7175-' + translit_string_full + '-2020.html'
    print(translit_string)


movie_online('привет')

if __name__ == "transliterate":
    transliterate()