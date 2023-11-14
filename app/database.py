import sqlite3 as sq

db = sq.connect('swallow.db')
cur = db.cursor()


async def start_db():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id UNIQUE NOT NULL INTEGER)")
    db.commit()


# проверяет наличие такого айди в базе, его отсутствие означает создание
async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()