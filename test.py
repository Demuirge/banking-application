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
name = "demuirge"
name2 = "ironman"
account_number = cursor.execute("""
SELECT account_number FROM customer_database WHERE username = ? ;
""", (name,)).fetchone()

balance = cursor.execute("""
SELECT balance FROM customer_database WHERE username = ? ;
""", (name,)).fetchone()

59419938

account_number2 = cursor.execute("""
SELECT account_number FROM customer_database WHERE username = ? ;
""", (name2,)).fetchone()

print(account_number)
print(balance)
print(account_number2)

85718744