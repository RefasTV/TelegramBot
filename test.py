import sqlite3

try:
    conn = sqlite3.connect("dataBase.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO `users` (`user_id`) VALUES (?)", (1000,))

    users = cursor.execute("SELECT * FROM `users`")
    print(users.fetchall())

    conn.commit()

except sqlite3.Error as error:
    print(error)


finally:
    if conn:
        conn.close()