# from datetime import datetime

# time = datetime.now()

# print(time)

# try:
#     ant = float(input("pick a number: "))
# except ValueError:
#     print("not valid as value")
# except TypeError:
#     print("not valid as type")

import sqlite3

conn = sqlite3.connect("customers_information.db")


cursor = conn.cursor()
cursor.execute(" PRAGMA foreign_keys = ON")
# name = "demuirge"
name2 = "ironman"
# account_number = cursor.execute("""
# SELECT account_number FROM customer_database WHERE username = ? ;
# """, (name,)).fetchone()

# balance = cursor.execute("""
# SELECT balance FROM customer_database WHERE username = ? ;
# """, (name,)).fetchone()

# 59419938

account_number2 = cursor.execute("""
SELECT account_number FROM customer_database WHERE username = ? ;
""", (name2,)).fetchone()

for num in account_number2:
    num = num

print(num)

# print(account_number)
# print(balance)
# print(account_number2)

# 85718744

# conn = sqlite3.connect("customer.db")

# cursor = conn.cursor()

# # noun = input("input a name for the table: ")

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS noun (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     full_name TEXT NOT NULL,
#     username TEXT NOT NULL UNIQUE
# )
# """)

# full_name = input("enter your name: ")
# username = input("enter your username: ")

# cursor.execute("""
# INSERT INTO noun (full_name, username) VALUES
# (?, ?);
# """, (full_name, username))

# one = cursor.execute("""
# SELECT full_name, username FROM noun;
# """).fetchall()

# print(one)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS transaction_history (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     account_number INTEGER NOT NULL UNIQUE,
#     transaction_description TEXT NOT NULL,
#     FOREIGN KEY(account_number) REFERENCES customer_database(account_number)
# )
# """)

desc = "withdrawal"
num2 = 45678123

# cursor.execute("""
# INSERT INTO transaction_history (account_number, transaction_description) VALUES 
# (?, ?);
# """, (num, desc))

# test = cursor.execute("""
# SELECT * FROM transaction_history WHERE account_number = ?;
# """, (num2,)).fetchone()

# print(test)

# cursor.execute("""
# DELETE * FROM transaction_history WHERE account_number = ?;
# """, (num,))

# test = cursor.execute("""
#  SELECT * FROM transaction_history WHERE account_number = ?;
# """, (num,)).fetchone()

# print(test)

# cursor.execute("DROP TABLE transaction_history")

# print("table dropped")

# 97677327
# 45640734
# 36170333