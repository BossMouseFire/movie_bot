import os
from dotenv import load_dotenv
from vkbottle import Bot
from routes import cinema_park, event
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.environ.get("SECRET_KEY")
bot = Bot(TOKEN)

bot.set_blueprints(cinema_park.bp, event.bp)


bot.run_polling()
