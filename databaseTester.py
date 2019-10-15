import sqlite3
import hashlib


conn = sqlite3.connect('users.db')
cur = conn.cursor()
try:
    user = cur.execute("SELECT * FROM users;").fetchall()
    print("Email = " + user[0][0])
    print("Name = " + user[0][1])
    print("Pass = " + user[0][2])
    print("Salt = " + str(user[0][3]))

    salt = user[0][3]
    hash = hashlib.sha512()
    hash.update(('%s%s' % (salt, user[0][2])).encode('utf-8'))
    hashPass = hash.hexdigest()
    print("Hashed/Salted Pass = " + hashPass)
except:
    print("Error is ")
