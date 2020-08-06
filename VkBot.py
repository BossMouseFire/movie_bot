import vk_api.vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
TOKEN = os.environ.get("SECRET_KEY")

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk)
