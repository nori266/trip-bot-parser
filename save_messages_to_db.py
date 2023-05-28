import os
import re

from dotenv import load_dotenv
# events and sync should be imported to avoid the error:
# TypeError: 'coroutine' object is not iterable
from telethon import TelegramClient, events, sync
from tqdm.asyncio import tqdm

from database import createDB, getDBconn, insert_message

"""
Message examples:
#водитель #вфинляндию

☎️ Связаться (Телеграм): @nickname1, Name1 #id400000000
💶 Цена: 100
🗓 Дата: 04.06.2023
💺 Мест: 3
Оᴛ ʍᥱᴛρ᧐ 𐌿ρ᧐ᥴʙᥱщᥱнᥙя дᴏ ʙᴀɯᴇᴦᴏ ᴀдᴩᴇᴄᴀ ʙ Финᴧяндии. Выᴇɜд ʙ 14.00 BMW X5. Чиᴛᴀйᴛᴇ ᴏᴛɜыʙы.

💬 Написать отзыв о попутчике Name1

 Отправить свою заявку через бот: @botname
 
#пассажир #вфинляндию

☎️ Связаться (Телеграм): @nickname2, Name2 #id100000000
💶 Цена: 35
🗓 Дата: 30.05.2023
💺 Мест: 1
Нужна машина из спб или выборга после обеда до Virolahti бюджет

💬 Написать отзыв о попутчике Name2

 Отправить свою заявку через бот: @botname
"""


load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

LAST_MESSAGES_NUMBER = 10000
BOT_NAME = "rus_fin_kyyti"  # TODO to env
# TODO desired date pattern as a command line argument
TRIP_DATE_PATTERN = re.compile(r"Дата: (\d\d.\d\d.\d\d\d\d)")  # group 1 should be a date


def get_last_n_mes(n=LAST_MESSAGES_NUMBER):
    client = TelegramClient('parse_session', api_id, api_hash)
    client.start()
    return client.get_messages('rus_fin_kyyti', limit=n)


def extract_trip_date(message):
    search = TRIP_DATE_PATTERN.search(message)
    if search:
        date = search.group(1)
        return date
    else:
        return None


def extract_hashtags(message):
    to_russia = "#вроссию" in message
    to_finland = "#вфинляндию" in message
    is_driver = "#водитель" in message
    return to_russia, to_finland, is_driver


createDB("./tg_drivers_bot.db")

dbConnection = getDBconn("./tg_drivers_bot.db")
dbCursor = dbConnection.cursor()


for mes in tqdm(get_last_n_mes()):
    if not mes.message:
        continue
    trip_date = extract_trip_date(mes.message)
    torussia, tofinland, isdriver = extract_hashtags(mes.message)
    if not (torussia or tofinland):
        continue
    insert_message(dbCursor, mes, trip_date, torussia, tofinland, isdriver)


dbConnection.commit()
dbConnection.close()
