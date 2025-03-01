import hashlib
import re
import time

from getpass import getpass



def interface():

    def sign_up():
        print("\nWelcome to the Sign Up page. Please fill in the form below and we will set up your account in no time!\n")

        time.sleep(0.5)

        while True:
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

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        while True:
            try:
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
            pass

try:
    interface()
except KeyboardInterrupt:
    print("\nYou quit the application.")
except Exception:
    pass