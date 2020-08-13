import sqlite3
import time
db = sqlite3.connect('bot.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS vkUsers(
id TEXT,
date_accession TEXT
)""")
db.commit()


def type_time(v):
    return time.strftime(v)


def information(users_name):
    users_data = type_time("%Y") + "-" + type_time("%m") + "-" + type_time('%d')
    sql.execute(f"SELECT id FROM vkUsers WHERE id = '{users_name}'")
    if sql.fetchone() is None:
        sql.execute(f'INSERT INTO vkUsers VALUES (?, ?)', (users_name, users_data))
        db.commit()

    else:
        print("Запись имеется")
        for value in sql.execute("SELECT * FROM vkUsers"):
            print(value)

