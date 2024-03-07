import sqlite3
from datetime import date as dt


class DBBot:
    def __init__(self, bd_file) -> None:
        self.conn = sqlite3.connect("dataBase.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
		
    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id, ))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id, ))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id, ))
        return self.conn.commit()
    
    def add_record(self, user_id, value, place, category):
        self.cursor.execute("INSERT INTO `records` (`user_id`, `value`, `place`, `category`, `date`) VALUES (?, ?, ?, ?, ?)", (self.get_user_id(user_id), value, place, category, dt.today()))
        return self.conn.commit()
    
    def get_records(self, user_id):
        id = self.get_user_id(user_id)
        result = self.cursor.execute("SELECT * FROM `records` WHERE `user_id` = ?", (id, ))

        print(result.fetchall)
        return result.fetchall()
    
    def get_categories(self, user_id):
        wasCat = []
        id = self.get_user_id(user_id)
        categ = self.cursor.execute("SELECT `category` FROM `records` WHERE `user_id` = ?", (id, ))
        categ = categ.fetchall()
        ret = []

        for r in categ:
            if r not in wasCat:
                ret.append(r)
                wasCat.append(r)

        return ret
    
    def get_records_by_categories(self, cat, user_id):
        id = self.get_user_id(user_id)
        print(cat,id)
        result = self.cursor.execute("SELECT * FROM `records` WHERE (`user_id`, `category`) = (?, ?)", (id, cat))
        print(result)
        return result.fetchall()
    
    def get_places(self, user_id):
        wasCat = []
        id = self.get_user_id(user_id)
        categ = self.cursor.execute("SELECT `place` FROM `records` WHERE `user_id` = ?", (id, ))
        categ = categ.fetchall()
        ret = []

        for r in categ:
            if r not in wasCat:
                ret.append(r)
                wasCat.append(r)

        return ret
    
    def get_records_by_places(self, place, user_id):
        id = self.get_user_id(user_id)
        result = self.cursor.execute("SELECT * FROM `records` WHERE (`user_id`, `place`) = (?, ?)", (id, place))
        return result.fetchall()

    def close(self):
        self.conn.close()
