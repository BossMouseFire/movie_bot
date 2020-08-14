import sqlite3
import time
db = sqlite3.connect('bot.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS vkUsers(
id TEXT,
date_accession TEXT,
city TEXT
)""")
db.commit()


def type_time(v):
    return time.strftime(v)


def information(users_id, user_city):
    users_data = type_time("%Y") + "-" + type_time("%m") + "-" + type_time('%d')
    sql.execute(f"SELECT id FROM vkUsers WHERE id = '{users_id}'")
    if sql.fetchone() is None:
        sql.execute(f'INSERT INTO vkUsers VALUES (?, ?, ?)', (users_id, users_data, user_city))
        db.commit()

    else:
        update_city(users_id, user_city)


def update_city(user_id, user_city):  # Обновление местоположения человека
    sql.execute(f"UPDATE vkUsers SET city = '{user_city}' WHERE id = '{user_id}'")
    db.commit()


def check_person(users_id):
    sql.execute(f"SELECT id FROM vkUsers WHERE id='{users_id}'")
    if sql.fetchone() is None:
        return 0
    else:
        return 1


def get_city(user_id):
    city = sql.execute(f"SELECT city FROM vkUsers WHERE id = '{user_id}'")
    return city.fetchone()[0]