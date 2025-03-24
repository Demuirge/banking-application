import hashlib
import re
import sqlite3
import time

from datetime import datetime
from getpass import getpass
from random import randint

conn = sqlite3.connect("customers_information.db", detect_types=sqlite3.PARSE_DECLTYPES |sqlite3.PARSE_COLNAMES)
cursor = conn.cursor()


ansi_escape = re.compile(r'\033\[[0-9;]*m')


def visible_length(text):
    """Returns the visible length of a string after removing ANSI escape codes."""
    return len(ansi_escape.sub('', text))

def insert_into_transaction_history(account_number,transaction_description,amount,balance):
    try:
        cursor.execute("""
                INSERT INTO transaction_history (account_number, transaction_description, amount, balance) VALUES
                (?, ?, ?, ?);
                """,(account_number,transaction_description, amount, balance))
    except Exception as e:
        print(e)

def amount_validation(operation):
    while True:
        try:
            amount = float(input(f"\nHow much would you like to {operation}? ").strip())
            if not amount:
                print("\nInput field cannot be empty")
                continue
            elif amount < 0:
                print("\nAmount cannot be negative")
                continue
        except (ValueError, TypeError):
            print("\nInvalid input. The amount needs to be in figures.")
            continue
        except Exception as e:
            print(f"\nSome error occured, {e}, please try again.")
            continue
        else:
            return amount

def balance_statement(username):
    balance = cursor.execute("""
    SELECT balance FROM customer_database WHERE username = ?;
    """, (username,)).fetchone()[0]

    print(f"\nYour available balance is now {balance} naira.")

class BankAccount:
    def __init__(self, username):
        # self.full_name = full_name
        self.username = username
        # self.account_number = account_number


    def deposit(self):
        # To make a deposit
        account_self = cursor.execute("""
        SELECT account_number FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]
        
        full_name = cursor.execute("""
        SELECT full_name FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]
        
        description = f"Deposit by {full_name}({account_self})"

        amount = amount_validation("deposit")

        balance = cursor.execute("""
        SELECT balance FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]

        balance += amount
        
        cursor.execute("""
        UPDATE customer_database
        SET balance = ?
        WHERE username = ?;
        """, (balance, self.username))

        conn.commit()

        time.sleep(3)
        print("\nDeposit successful")

        balance_statement(self.username)
        
        insert_into_transaction_history(account_self, description, amount, balance)

        conn.commit()

        time.sleep(1)

    def withdrawal(self):
        # To make a waithdrawal
        balance = cursor.execute("""
        SELECT balance FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]
        
        account_self = cursor.execute("""
        SELECT account_number FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]
        
        full_name = cursor.execute("""
        SELECT full_name FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]

        
        description = f"Withdrawal by {full_name}({account_self})"

        while True:
            amount = amount_validation("withdraw")
            if amount > balance:
                # To ensure more money than what is available cannot be withdrawn
                print("\nSorry you cannot withdraw more than you have in savings.")
                continue
            balance -= amount
            break

        cursor.execute("""
        UPDATE customer_database
        SET balance = ?
        WHERE username = ?;
        """, (balance, self.username))

        conn.commit()

        time.sleep(3)
        print("\nWithdrawal successful")


        balance_statement(self.username)
        
        insert_into_transaction_history(account_self, description, amount, balance)

        conn.commit()

        time.sleep(1)
    
    def transfer(self):
        # To transfer to another account
        account_self = cursor.execute("""
        SELECT account_number FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]
        
        full_name = cursor.execute("""
        SELECT full_name FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]
        
        while True:
            try:
                account_target = int(input("\nType the account number you would like to transfer to(Press 108 t0 cancel transfer): ").strip())
                if not(len(str(account_target)) == 8):
                    print(f"\nWe require a valid account number")
                    continue
                elif account_target == account_self:
                    print("\nCannot transfer to oneself.")
                    continue
                else:
                    balance_other = cursor.execute("""
                    SELECT balance FROM customer_database WHERE account_number = ?;
                    """, (account_target,)).fetchone()[0]
                    if not balance_other:
                        print("\nAccount number does not exist.")
                        continue
            except (ValueError):
                print("\nWe require a valid account number")
                continue
            except Exception as e:
                print(f"\nSomething went wrong {e}, please try again.")
                continue
            break

        balance = cursor.execute("""
        SELECT balance FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]

        account_target_full_name = cursor.execute("""
        SELECT full_name FROM customer_database WHERE account_number = ?;
        """, (account_target,)).fetchone()[0]

        while True:
            amount = amount_validation("transfer")
            if amount > balance:
                # To ensure more money than what is available cannot transferred
                print("\nSorry you cannot transfer more than you have in savings.")
                continue
            else:
                while True:
                    try:
                        confirmation = input(f"\nYou are about to transfer ₦{amount} to {account_target_full_name}({account_target}). Are you sure you want to proceed(Yes/No)? ").lower().strip()
                        if confirmation not in ("yes", "no"):
                            print("\nAnswer with Yes or No")
                            continue
                        elif confirmation == "yes":
                            balance -= amount
                            balance_other += amount
                            break
                        elif confirmation == "no":
                            print("\nCancelling Transfer")
                            time.sleep(1)
                            return
                    except (ValueError, TypeError):
                        print("\nYou have to confirm with a valid answer, Yes or No")
                        continue
                    except Exception as e:
                        print(f"\nSomething occured, {e}, please try again")
                        continue
                break        
        
        description = f"Transfer to {account_target_full_name}({account_target})"
        other_description = f"Transfer from {full_name}({account_self})"

        cursor.execute("""
        UPDATE customer_database
        SET balance = ?
        WHERE username = ?;
        """, (balance, self.username))

        insert_into_transaction_history(account_self, description, amount, balance)
        
        cursor.execute("""
        UPDATE customer_database
        SET balance = ?
        WHERE account_number = ?;
        """, (balance_other, account_target))

        insert_into_transaction_history(account_target, other_description, amount, balance_other)

        conn.commit()

        time.sleep(3)
        print("\ntransfer successful")

        balance_statement(self.username)
        time.sleep(1)
    
    def inquiry(self):
        # To check one's balance
        print("\nBringing up your balance, please wait.")

        time.sleep(2)

        balance_statement(self.username)
        time.sleep(1)

    def details(self):
        # To check one's account details, revealing their full name, username and account number
        print("\nBringing up your account details, please wait.")

        time.sleep(2)

        details = cursor.execute("""
        SELECT full_name, username, account_number FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()

        full_name, username, account_number = details
        
        account_details = f"""
FULL NAME : {full_name}
USERNAME : {username}
ACCOUNT NUMBER : {account_number}
"""
        print(account_details)
        time.sleep(1)

    def transaction_history(self):
        # To create a Transaction history table holding all the transactions of the user
        print("\nBringing up your transaction history, please wait.")
        time.sleep(2)

        account_self = cursor.execute("""
        SELECT account_number FROM customer_database WHERE username = ?;
        """, (self.username,)).fetchone()[0]

        histories = cursor.execute("""
        SELECT transaction_description, amount, balance, date_time FROM transaction_history WHERE account_number = ?;
        """, (account_self,)).fetchall()

        if not histories:
            print("No Transaction History")
            time.sleep(3)
        else:
            print("\n           Transaction History\n")
            header = ["Transaction Description", "Credit", "Debit", "Available Balance", "Transaction Period"]  # Header for the Transaction history table
            print(f"{header[0]:<60} || {header[1]:<15} || {header[2]:<15} || {header[3]:<20} || {header[4]:<20}")
            print("=" * 150)
            for history in histories:
                credit = " "
                debit = " "
                h2 = f"₦{history[2]:.2f}"
                if "Deposit" in history[0] or "deposit" in history[0]:
                    # This means an increase in the balance of the user, hence a credit
                    credit = f"\033[32m₦{history[1]:.2f}\033[0m"
                elif "Withdrawal" in history[0]:
                    # This means a decrease in the balance of the user, hence a debit
                    debit = f"\033[31m₦{history[1]:.2f}\033[0m"
                elif "Transfer" in history[0] and "from" in history[0]:
                    # This means an increase in the balance of the user, hence a credit
                    credit = f"\033[32m₦{history[1]:.2f}\033[0m"
                elif "Transfer" in history[0] and "to" in history[0]:
                    # This means a decrease in the balance of the user, hence a debit
                    debit = f"\033[31m₦{history[1]:.2f}\033[0m"
                    
                credit_padding = 15 + (len(credit) - visible_length(credit))
                debit_padding = 15 + (len(debit) - visible_length(debit))
                print(f"{history[0]:<60} || {credit:<{credit_padding}} || {debit:<{debit_padding}} || {h2:<20} || {history[3]:<20}") # The rows of the table
            time.sleep(3)


def interface():

    cursor.execute(" PRAGMA foreign_keys = ON") #To activate Foreign Key


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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaction_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number INTEGER NOT NULL,
        transaction_description TEXT NOT NULL,
        amount FLOAT NOT NULL,
        balance NUMERIC NOT NULL,
        date_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(account_number) REFERENCES customer_database(account_number)
    )
    """)
    

    def create_account_number():
        print("hello")
        #To create unique and random 8-digit numbers to act as account numbers for users
        while True:
            acct_num = randint(10000000, 99999999)
            print(acct_num)
            acct_nums = cursor.execute("""
            SELECT account_number from customer_database WHERE account_number = ?;
            """, (acct_num,)).fetchone()
            print(acct_num)
            if acct_nums is None:
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

            pattern = r"^[A-Za-z]{2,}\s[A-Za-z]{2,}(?:\s[A-Za-z]{2,})?$"

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
            except (ValueError, TypeError):
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
        
        account_number = create_account_number()

        try:
            print(f"account_number: {account_number}")
            #To input the user's data into the database and check for errors.
            cursor.execute("""
            INSERT INTO customer_database (full_name, username, password, balance, account_number) VALUES
            (?, ?, ?, ?, ?);
            """, (full_name, username, hashed_password, balance, account_number))
            print(f"account_number2: {account_number}")
        except sqlite3.IntegrityError:
            print("\nA user with that username already exists.")
            return None
        else:
            time.sleep(2)
            print("\nSign up successful")
            conn.commit()

            account_number = cursor.execute("""
            SELECT account_number FROM customer_database WHERE username = ?;
            """, (username,)).fetchone()[0]
            
            description = "Initial deposit"

            insert_into_transaction_history(account_number, description, balance, balance)
            conn.commit()

            time.sleep(2)
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
                # Enter into your account
                bank_operations(username)
                break
    
    def bank_operations(username):
        # To select which bank operation you would ike to undertake
        print("\nYou are now logged in")
        time.sleep(1)
        print(f"\nWelcome {username}")
        time.sleep(1)
        demuirge = BankAccount(username)
        menu2 = """
    1. Deposit
    2. Withdrawal
    3. Transfer
    4. Balance Inquiry
    5. Account Details
    6. Transaction History
    7. Log out
    """
        while True:
            print(menu2)
            time.sleep(1)
            choice = input("Choose the number from the options above the action you wish to take: ").strip()

            if choice == "7":
                print("\nThank you for patronising with us. We hope you had a great experience. Have a nice day!")
                time.sleep(0.5)
                break

            if choice not in ["1", "2", "3", "4", "5", "6"]:
                print("\nChoice is invalid")
                time.sleep(0.5)
                continue

            if choice == "1":
                time.sleep(1)
                demuirge.deposit()
            elif choice == "2":
                time.sleep(1)
                demuirge.withdrawal()
            elif choice == "3":
                time.sleep(1)
                demuirge.transfer()
            elif choice == "4":
                time.sleep(1)
                demuirge.inquiry()
            elif choice == "5":
                time.sleep(1)
                demuirge.details()
            elif choice == "6":
                time.sleep(1)
                demuirge.transaction_history()

    welcome_message = """
    Welcome to Demuirge Savings, your most trusted and secure bank in the region.
    We work with State-of-the-art technology and software to ensure your bank transacations are not only
    safe and secure, but also incredibly convenient to give you the best of experiences. We trust that you
    will continue to patronise with us. Thank you in advance.
    """

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
    print("\n\nYou quit the application.")
except Exception as e:
    print(f"Something occured, {e}, please try again.")
finally:
    conn.close()