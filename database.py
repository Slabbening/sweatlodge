import datetime
import sqlite3
import hashlib
import os


class DataBase:
    def __init__(self, conn):
        self.conn = sqlite3.connect(conn)
        self.users = None
        self.load()

    def load(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(20) UNIQUE, name VARCHAR(50), passw BLOB, salt BLOB, createdOn DATE); ")
        self.conn.commit()

    def get_user(self, username):
        try:
            self.conn.execute("SELECT username FROM users WHERE (username = ?);", (username,))
            self.conn.commit()
            return 1
        except sqlite3.Error:
            return -1

    def add_user(self, username, password, name):
        if len(list(password)) <= 6:
            return 2
        else:
            salt = os.urandom(32)
            hash = hashlib.sha512()
            hash.update(('%s%s' % (salt, password)).encode('utf-8'))
            hashPass = hash.hexdigest()
            try:
                self.conn.execute("INSERT INTO users (username, name, passw, salt, createdOn) VALUES (?, ?, ?, ?, ?)",
                                  (username, name, hashPass, salt, self.get_date()))
                self.conn.commit()
                return 1
            except sqlite3.Error:
                return -1


    def validate(self, username, password):
        user = self.conn.execute("SELECT * FROM users WHERE (username = ?);", (username,)).fetchall()
        if user:
            salt = user[0][3]
            hash = hashlib.sha512()
            hash.update(('%s%s' % (salt, password)).encode('utf-8'))
            hashPass = hash.hexdigest()
            if hashPass == str(user[0][2]):
                return True
            else:
                return False
        else:
            return False


    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]