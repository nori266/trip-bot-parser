from collections import Counter
import os
import re

from dotenv import load_dotenv
# events and sync should be imported to avoid the error:
# TypeError: 'coroutine' object is not iterable
from telethon import TelegramClient, events, sync

# from database import createDB, getDBconn, insert_message


load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")


def get_last_n_mes(n=100):

    client = TelegramClient('parse_session', api_id, api_hash)
    client.start()
    chat = client.get_input_entity('username')
    return client.get_messages('rus_fin_kyyti', limit=n)

# createDB()
#
# dbConnection = getDBconn()
# dbCursor = dbConnection.cursor()


date_counter = Counter()
for mes in get_last_n_mes():
    # insert_message(dbCursor, mes)
    pattern = re.compile(r"Дата: ((24).\d\d.202\d)")
    try:
        search = pattern.search(mes.message)
    except TypeError:
        print(mes.message)
    if search:
        date = search.group(1)
        if "#вфинляндию" in mes.message and "#водитель" in mes.message:
            print(mes.message)
            date_counter[date] += 1

print(date_counter.most_common(10))

# dbConnection.commit()
# dbConnection.close()





# relevant_msg_count = 0
    # if "19.06" in mes.message and "#водитель" in mes.message and "#вроссию" in mes.message:
    #     relevant_msg_count += 1
    #     print(mes.message, mes.from_id)


# В какие дни недели чаще ездят?
# За сколько дней обычно размещают водители?
# статистика за нужные мне дни в прошлом году
