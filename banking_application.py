import hashlib
import re
import sqlite3
import time

from getpass import getpass
from random import randint

conn = sqlite3.connect("customers_information.db")


def interface():

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_database (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        balance NUMERIC NOT NULL,
        account_number INTEGER NOT NULL UNIQUE
    )
    """)

    def account_numbers():
        #To create unique and random 8-digit numbers to act as account numbers for users
        acct_num = randint(23456789, 98765432)
        accct_nums = cursor.execute("""
        SELECT account_number from customer_database;
        """)
        while True:
            if acct_num in accct_nums:
                acct_num = randint(23456789, 98765432)
                continue
            return acct_num

    def sign_up():
        #Creating a sign up function to take in inputs of information from prospective user and put into a database 

        print("\nWelcome to the Sign Up page. Please fill in the form below and we will set up your account in no time!\n")

        time.sleep(0.5)

        while True:
            #To take in user's fullname in the order of Surname, First Name and Middle Name.
            full_name = input("Please give us your Full Name in the following order (Surname First Name Middle Name): ").title().strip()


            if not full_name:
                print("\nField is required\n")
                continue
            if not (5 <= len(full_name) <= 255):
                print("\nYour name has to be a minimum of 4 characters and maximum of 255\n")
                continue

            pattern = r"^[a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]+$"

            if not re.match(pattern, full_name):
                print("\nYour full name has to be written with no error\n")
                continue

            break
        
        while True:
            #To take in user's Username
            username = input("\nCreate a Username: ").strip()
            pattern = r"^[a-zA-Z0-9_]+$"

            if not username:
                print("\nField is required")
                continue

            if not (3 <= len(username) <= 20):
                print("\nYour name has to be a minimum of 3 characters and maximum of 20")
                continue

            if not re.match(pattern, username):
                print("\nYour username can only contain alphanumeric characters and underscores")
                continue

            break

        while True:
            #To create a valid and strong password
            password = getpass("\nCreate your password: ").strip()

            if not password:
                print("\nPassword field is required")
                continue

            if not (8 <= len(password) <= 30):
                print("\nYour password must have a minimum of 8 characters and a maximum of 30")
                continue

            if re.search("[!+*?#~$%^&@;]", password) is None:
                print("\nPassword requires special characters")
                continue
            elif re.search("[a-zA-Z]", password) is None:
                print("\nPassword requires alphabetic characters")
                continue
            elif re.search("[0-9]", password) is None:
                print("\nPassword requires numeric characters")
                continue

            confirm_password = getpass("\nConfirm your password: ").strip()
            if not confirm_password:
                print("\nConfirm Password field is required")
                continue

            if password != confirm_password:
                print("\nPasswords do not match")
                continue
            break

        #To hide the password even in the database.
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        while True:
            try:
                #To take in an initial deposit in order to activate user's account.
                initial_deposit = float(input("\nPut in an initial deposit in order to activate your account. It must not be less than 2000: "))
            except ValueError or TypeError:
                print("\nYou need to input a valid deposit in figures.")
                continue
            else:
                if initial_deposit < 0:
                    print("\nInitial Deposit cannot be negative")
                    continue
                elif initial_deposit < 2000:
                    print("\nA minimum amount of 2000 naira is required")
                    continue
                balance = initial_deposit
            break

        try:
            #To input the user's data into the database and check for errors.
            cursor.execute("""
            INSERT INTO customer_database (full_name, username, password, balance, account_number) VALUES
            (?, ?, ?, ?, ?);
            """, (full_name, username, hashed_password, balance, account_numbers()))
        except sqlite3.IntegrityError:
            print("\nA user with that username already exists.")
            return None
        else:
            print("\nSign up successful")
            conn.commit()
            log_in()
    
    def log_in():
        #To log into using username and password as long as it exists in the database
        print("\n Welcome customer to the Log in page. Please fill in your username and password.\n")
        
        while True:
            #To validate the username and password
            username = input("\nEnter your username: ").strip()
            if not username:
                print("\nField is required")
                continue
            
            while True:
                password = getpass("\nEnter your password: ").strip()
                if not password:
                    print("\nField is required")
                    continue
                break

            hashed_password = hashlib.sha256(password.encode()).hexdigest()


            user = cursor.execute("""
            SELECT * FROM customer_database WHERE username = ? AND password = ?;
            """, (username, hashed_password)).fetchone()

            if user is None:
                print("\nInvalid username or password.")
                continue
            else:
                time.sleep(1)
                print("\nLog in Successful")
                pass

    welcome_message = """
    Welcome to Demuirge Savings, your most trusted and secure bank in the region.
    We work with State-of-the-art technology and software to ensure your bank transacations are not only
    safe and secure, but also incredibly convenient to give you the best of experiences. We trust that you
    will continue to patronise with us. Thank you in advance."""

    menu = """
    1. Sign Up
    2. Log In
    3. Exit
    """

    print(welcome_message)
    time.sleep(1)

    while True:
        print(menu)
        time.sleep(1)
        choice = input("Choose the number from the options above the action you wish to take: ").strip()

        if choice == "3":
            print("\nThank you for patronising with us. We hope you had a great experience. Have a nice day!")
            time.sleep(0.5)
            break

        if choice not in ["1", "2"]:
            print("\nChoice is invalid")
            time.sleep(0.5)
            continue

        if choice == "1":
            sign_up()
        elif choice == "2":
            log_in()

try:
    interface()
except KeyboardInterrupt:
    print("\nYou quit the application.")
except Exception:
    pass