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
balance = cursor.execute("""
SELECT balance FROM customer_database WHERE username = ? ;
""", (name,)).fetchone()

print(balance)